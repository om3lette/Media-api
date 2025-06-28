<script setup lang="ts">
import InputGroup from "primevue/inputgroup";
import InputGroupAddon from "primevue/inputgroupaddon";
import InputText from "primevue/inputtext";
import Button from "primevue/button";
import { useI18n } from "vue-i18n";
import { ref, computed, watch } from "vue";
import { useSourceStore } from "@/stores/sourceStore";
import { isValidURL } from "@/utils";
import emitter from "@/plugins/emitter";
import { getResponseStatus } from "@/api/utils";
const { t } = useI18n();

const urlInput = ref<string>("");
const sourceStore = useSourceStore();
watch(urlInput, (value: string) => sourceStore.setUrl(value));

const loadingState = ref<boolean>(false);

const checkUrlIcon = ref<string>("globe");
const urlButtonClass = computed(() => `pi pi-${checkUrlIcon.value}`);
const urlButtonSeverity = ref<string>("contrast");
let buttonResetTimeout: number;

emitter.on("process-request-sent", () => {
  urlInput.value = "";
});

const resetButtonStyle = () => {
  checkUrlIcon.value = "globe";
  urlButtonSeverity.value = "contrast";
};

const checkIfReachable = async () => {
  clearTimeout(buttonResetTimeout);
  resetButtonStyle();

  loadingState.value = true;
  const isReachable = await isFileReachable(urlInput.value);
  checkUrlIcon.value = isReachable ? "check" : "times";
  urlButtonSeverity.value = isReachable ? "success" : "danger";
  loadingState.value = false;
  buttonResetTimeout = setTimeout(resetButtonStyle, 3500);
};

const isFileReachable = async (url: string) => {
  try {
    if (!isValidURL(url)) return false;
    return (await getResponseStatus(url)) == 200;
  } catch (_) {
    return false;
  }
};
</script>

<template>
  <div>
    <label for="url-input">{{ t("process.source.enter-url") }}</label>
    <InputGroup id="url-input">
      <InputText
        :disabled="loadingState"
        v-model="urlInput"
        placeholder="https://example.com/video.mp4"
      />
      <InputGroupAddon>
        <Button
          @click="checkIfReachable"
          :loading="loadingState"
          :icon="urlButtonClass"
          :severity="urlButtonSeverity"
          :label="t('process.source.check-url')"
        />
      </InputGroupAddon>
    </InputGroup>
  </div>
</template>
