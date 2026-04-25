<script setup>
import { useI18n } from "vue-i18n";
import Message from "primevue/message";
import SettingsStepper from "./SettingsStepper.vue";
const { t } = useI18n();
</script>
<template>
  <div class="border-3 border-surface-200 bg-surface-0 p-4 rounded-md space-y-2 dark:bg-surface-600 dark:border-surface-700">
    <div>
      <h2>{{ t("process.settings.title") }}</h2>
      <Message size="small" variant="simple" severity="secondary">{{
        t("process.settings.description")
      }}</Message>
    </div>
    <SettingsStepper />
  </div>
</template>
