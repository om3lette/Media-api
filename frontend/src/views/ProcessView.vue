<script setup lang="ts">
import { provide, ref, computed, onMounted } from "vue";
import { useI18n } from "vue-i18n";
import SourceInput from "@/components/process/sourceInput/SourceInput.vue";
import OperationsInput from "@/components/process/operationsInput/OperationsInput.vue";
import ProcessSettings from "@/components/process/settings/ProcessSettings.vue";
import HistoryDrawer from "@/components/process/HistoryDrawer.vue";
import { settingsOptions } from "@/constants/settingsOptions";
import { Button } from "primevue";
import type { Operation, Operations } from "@/types/types";
import { useSourceStore } from "@/stores/sourceStore";
import { useSettingsStore } from "@/stores/settingsStore";
import { useOperationsStore } from "@/stores/operationsStore";
import { isValidURL } from "@/utils";
import emitter from "@/plugins/emitter";
import toastWrapper from "@/plugins/toastWrapper";
import { useHistoryStore } from "@/stores/historyStore";
import { getRequestStatus, getSubPayload, getSyncPayload, getUnSubPayload } from "@/api/status";

import Toast from "primevue/toast";
import { postNewRequest } from "@/api/upload";
import { useWebSocket } from "@vueuse/core";
import { getUrl } from "@/api/urlProvider";
import { UrlType } from "@/types/api";
import { watch } from "vue";
import type {
  SyncPayload,
  StatusPayload,
  ProgressPayload,
  StagePayload,
  ErrorPayload,
  RequestCreatedPayload
} from "@/types/api";
import { useNotification } from "@/composables/useNotification";

const settingsStore = useSettingsStore();
const sourceStore = useSourceStore();
const operationsStore = useOperationsStore();
const historyStore = useHistoryStore();

const resetStores = () => {
  settingsStore.$reset();
  sourceStore.$reset();
  operationsStore.$reset();
};
const syncRequestState = async (rid: string): Promise<SyncPayload | undefined> => {
  const res = await getRequestStatus(rid);
  if (!res) return;
  const data: SyncPayload = await res.json();
  historyStore.syncRequestStatus(data);
  return data;
};
onMounted(async () => {
  resetStores();
  // Synchronize requests state
  for (const request of historyStore.getRequestsInProgress()) {
    await syncRequestState(request.id);
  }
});

const isDataProvided = computed<boolean>(
  () => sourceStore.isSourceSet() && operationsStore.size > 0
);

const { t } = useI18n();
const operations = ref<Operations>(["compress", "extract-audio", "transcribe", "summarize"]);

provide("availableOperations", operations);
provide("settingsOptions", settingsOptions);

const anyOperationSelected = (operationsToCheck: Operations) => {
  return operationsStore.selectedOperations.some((operation: Operation) =>
    operationsToCheck.includes(operation)
  );
};

const addDataIfOperationSelected = (
  data: Record<string, any>,
  key: string,
  value: any,
  operationsToCheck: Operations
) => {
  if (!anyOperationSelected(operationsToCheck)) return;
  data[key] = value;
};

const processButtonLoading = ref<boolean>(false);

const { send, data } = useWebSocket(getUrl(UrlType.WS_STATUS), { autoReconnect: true });

const { newNotification } = useNotification();

const handleStatusUpdate = async (rid: string, requestStatus: number) => {
  const historyEntry = historyStore.getRequestById(rid);
  if (!historyEntry) return false;

  switch (requestStatus) {
    case 0:
      return historyStore.updateStatus(rid, "queued");
    case 1:
      return historyStore.updateStatus(rid, "processing");
    case 2:
    case 3:
      await newNotification(t("process.history.notifications.status-update"), {
        body: t("process.history.notifications.request-completed", {
          filename: historyEntry.filename
        })
      });
      return historyStore.updateStatus(rid, "completed");
    default:
      await newNotification(t("process.history.notifications.status-update"), {
        body: t("process.history.notifications.request-canceled", {
          filename: historyEntry.filename
        })
      });
      return historyStore.updateStatus(rid, "canceled", true);
  }
};

watch(data, async () => {
  const parsedData = JSON.parse(data.value);

  if (parsedData.type === "error") {
    const payload: ErrorPayload = parsedData;

    if (payload.isValidation) {
      console.error(payload.code);
      toastWrapper.error(t("process.errors.validation-error"));
      return;
    }
    if (payload.isMissing) {
      historyStore.updateStatus(payload.rid, "deleted", true);
      return;
    }
    // Other errors are not critical
    return;
  }
  let isHistoryEntryPresent: boolean = false;

  switch (parsedData.type) {
    case "status": {
      const payload: StatusPayload = parsedData;
      isHistoryEntryPresent = await handleStatusUpdate(payload.rid, payload.status);
      break;
    }
    case "progress": {
      const payload: ProgressPayload = parsedData;
      isHistoryEntryPresent = historyStore.updateProgress(payload.rid, payload.pct);
      break;
    }
    case "stage": {
      const payload: StagePayload = parsedData;
      isHistoryEntryPresent = historyStore.updateStage(payload.rid, payload.curStage);
      break;
    }
    case "sync": {
      isHistoryEntryPresent = historyStore.syncRequestStatus(parsedData as SyncPayload);
      break;
    }
    default:
      console.warn(`Unknown event type: ${parsedData.type}`);
      break;
  }
  if (isHistoryEntryPresent) {
    if (!historyStore.isInitialized(parsedData.rid)) {
      // Get request metadata. E.g total stages
      send(getSyncPayload(parsedData.rid));
    }
    return;
  }
  // No data about the request found => stop tracking updates
  send(getUnSubPayload(parsedData.rid));
});

const submitRequest = async () => {
  let errorMessage: string = "";
  if (operationsStore.size < 1) {
    errorMessage = t("process.errors.no-operations-selected");
  } else if (!sourceStore.isSourceSet()) {
    errorMessage = t("no-source-provided");
  }

  if (errorMessage) {
    toastWrapper.error(errorMessage);
    return;
  }
  const requestData: Record<string, any> = {
    actions: operationsStore.selectedOperations.map((el) => el.replace("-", "_")),
    config: {}
  };

  // Add configs based on selected operations
  addDataIfOperationSelected(requestData.config, "ffmpeg", settingsStore.ffmpeg, ["compress"]);
  addDataIfOperationSelected(requestData.config, "audio", settingsStore.audio, ["extract-audio"]);
  addDataIfOperationSelected(requestData.config, "transcribe", settingsStore.transcribe, [
    "transribe"
  ]);

  const formData = new FormData();
  // Set source file / url / local path
  if (sourceStore.file) formData.append("file", sourceStore.file);
  else if (isValidURL(sourceStore.url)) requestData["url"] = sourceStore.url;
  else requestData["path"] = requestData["path"] = sourceStore.url;

  formData.append("data", JSON.stringify(requestData));

  processButtonLoading.value = true;
  const response = await postNewRequest(formData);
  processButtonLoading.value = false;

  switch (response.status) {
    case 200:
      // Request accepted
      break;
    case 400:
    case 422:
      errorMessage = t("process.errors.validation-error");
      break;
    case 503:
      errorMessage = t("process.errors.server-unavailable");
      break;
    case 409:
      errorMessage = t("process.errors.already-queued");
      break;
    default:
      errorMessage = t("process.errors.unknown-error");
      break;
  }
  if (errorMessage) {
    toastWrapper.error(errorMessage);
    return;
  }
  const requestId: string = ((await response.json()) as RequestCreatedPayload).rid;
  send(getSubPayload(requestId));

  historyStore.addEntry(
    requestId,
    JSON.parse(JSON.stringify(operationsStore.selectedOperations)),
    sourceStore.file?.name ?? t("process.history.remote-file")
  );
  emitter.emit("process-request-sent", null);
  resetStores();
  toastWrapper.success(t("process.request-sent"));
};

const visibleHistory = ref<boolean>(false);
</script>
<template>
  <section class="flex justify-center my-10">
    <div class="w-11/12 2xl:w-9/12 space-y-8">
      <nav class="flex justify-between items-center">
        <h1 class="max-w-2/3">{{ t("process.title") }}</h1>
        <Button
          @click="visibleHistory = true"
          label="История"
          icon="pi pi-history"
          severity="contrast"
          class="h-1/2"
        ></Button>
      </nav>
      <div
        class="flex flex-col items-center space-y-8 justify-around lg:flex-row lg:items-stretch lg:space-x-10 lg:space-y-0"
      >
        <SourceInput class="w-full lg:w-1/2" />
        <OperationsInput
          @submit="submitRequest"
          v-model:button-loading="processButtonLoading"
          :enable-process-button="isDataProvided"
          class="w-full lg:w-1/2"
        />
      </div>
      <ProcessSettings />
    </div>
    <HistoryDrawer v-model:visibility="visibleHistory" />
  </section>
  <Toast />
</template>
