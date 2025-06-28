<script setup lang="ts">
import type { SettingsOptions } from "@/types/settings/options";
import Select from "primevue/select";
import GridWrapper from "./GridWrapper.vue";
import InputWrapper from "./InputWrapper.vue";
import { inject, ref } from "vue";
import { useSettingsStore } from "@/stores/settingsStore";

const settingsStore = useSettingsStore();
const settingsOptions = inject<SettingsOptions>("settingsOptions")!;
const l = ref(settingsOptions.transcription.language);

defineProps<{ enableDivider?: boolean }>();
</script>

<template>
  <GridWrapper t-title="transcription.title" :divired="enableDivider ?? false" :one-column="true">
    <template #body>
      <InputWrapper id="transcription-language-input" t-selector="transcription.language">
        <Select
          :options="l"
          v-model="settingsStore.transcribe.language"
          id="transcription-language-input"
          option-label="label"
          option-value="value"
        />
      </InputWrapper>
    </template>
  </GridWrapper>
</template>
