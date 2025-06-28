<script setup lang="ts">
import { useI18n } from "vue-i18n";
import GridWrapper from "./GridWrapper.vue";

defineProps<{ enableDivider?: boolean }>();
const { t } = useI18n();
</script>

<template>
  <GridWrapper t-title="summarize.title" :divired="enableDivider ?? false" :one-column="true">
    <template #body>
      <div>{{ t("process.settings.no-settings-available") }}</div>
    </template>
  </GridWrapper>
</template>
