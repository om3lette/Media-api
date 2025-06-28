<script setup lang="ts">
import { useHistoryStore } from "@/stores/historyStore";
import type { RequestData } from "@/types/requests";
import { getIconByOperation, timestampToReadable } from "@/utils";
import { Button, Drawer, Chip, Divider } from "primevue";
import { computed } from "vue";
import { useI18n } from "vue-i18n";
import { useSize } from "@/composables/useSize";
import toastWrapper from "@/plugins/toastWrapper";

import { getRequestOutput } from "@/api/download";

const { t } = useI18n();
const visibility = defineModel<boolean>("visibility");
const historyStore = useHistoryStore();

const { windowSize } = useSize();
const reversedHistory = computed<RequestData[]>(() =>
  historyStore.history.slice().sort((a, b) => b.timestamp - a.timestamp)
);

async function downloadFile(requestId: string) {
  const response = await getRequestOutput(requestId);
  if (!response.ok) {
    toastWrapper.error(t("process.errors.request-expired"));
    historyStore.updateStatus(requestId, "completed", true);
    return;
  }

  const blob = await response.blob();
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = `${requestId}.zip`;
  link.click();
  URL.revokeObjectURL(link.href);
}

const drawerPosition = computed<string>(() =>
  ["xs", "sm", "md"].includes(windowSize.value) ? "full" : "right"
);
</script>

<template>
  <Drawer v-model:visible="visibility" :position="drawerPosition" class="lg:!w-4/9">
    <template #container="{ closeCallback }">
      <div class="w-full min-h-[100vh] overflow-y-auto flex flex-col space-y-3">
        <div class="px-6 pt-6 flex items-center justify-between">
          <span class="flex space-x-2 items-center">
            <i class="pi pi-history !text-xl"></i>
            <h2>{{ t("process.history.title") }}</h2>
          </span>
          <Button
            type="button"
            @click="closeCallback"
            severity="contrast"
            icon="pi pi-times"
            rounded
            outlined
          ></Button>
        </div>
        <div v-if="historyStore.history.length > 0">
          <Divider />
          <div v-for="entry in reversedHistory" :key="entry.id" class="flex flex-col">
            <div class="px-6">
              <div class="w-full flex justify-between items-center space-x-4">
                <h3 class="overflow-x-auto whitespace-nowrap">{{ entry.filename }}</h3>
                <Chip
                  class="text-sm xs:text-base"
                  :label="t(`process.history.status.${entry.status.toLowerCase()}`)"
                />
              </div>
              <div class="mb-3 space-y-2">
                <p>{{ timestampToReadable(entry.timestamp) }}</p>
                <div class="grid grid-cols-2 gap-2">
                  <Chip
                    class="!flex !justify-center text-sm xs:text-base"
                    v-for="operation in entry.operations"
                    :key="`operation-${operation}`"
                    :label="t(`process.operations.types.${operation}.title`)"
                    :icon="`pi pi-${getIconByOperation(operation)}`"
                  />
                </div>
              </div>
              <div
                v-if="entry.status == 'completed' && !entry.expired"
                class="w-full flex justify-center"
              >
                <Button
                  @click="async () => await downloadFile(entry.id)"
                  class="w-full"
                  :label="t('process.history.download')"
                  icon="pi pi-download"
                  severity="contrast"
                />
              </div>
              <div
                v-else-if="
                  entry.status === 'processing' && entry.totalStages > 0 && entry.currentStage > 0
                "
                class="flex flex-col space-y-1"
              >
                <div class="w-full flex justify-between">
                  <div class="space-x-1">
                    <span>{{ t("process.history.stage") }}</span>
                    <span>{{ entry.currentStage }}/{{ entry.totalStages }}</span>
                  </div>
                  <div>{{ entry.stageProgress }}%</div>
                </div>
                <div class="bg-gray-200 w-full h-3 rounded-full overflow-hidden relative">
                  <div
                    :style="`width: ${entry.stageProgress}%`"
                    class="absolute left-0 h-full bg-gray-800 ease-linear transition-all duration-300"
                  ></div>
                </div>
              </div>
            </div>
            <Divider />
          </div>
        </div>
      </div>
    </template>
  </Drawer>
</template>
