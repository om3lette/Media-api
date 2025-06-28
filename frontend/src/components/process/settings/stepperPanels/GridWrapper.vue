<script setup lang="ts">
import { useI18n } from "vue-i18n";
import Divider from "primevue/divider";
const { t } = useI18n();
defineProps<{ tTitle: string; divired?: boolean; oneColumn?: boolean }>();
</script>

<template>
  <Divider v-if="divired" />
  <h3 class="mb-2">{{ t(`process.settings.inputs.${tTitle}`) }}</h3>
  <div
    :class="{ 'lg:grid-cols-1': oneColumn, 'lg:grid-cols-2': !oneColumn }"
    class="grid grid-cols-1 lg:auto-cols-auto gap-y-4 gap-x-10"
  >
    <slot name="body"></slot>
  </div>
  <slot name="footer"></slot>
</template>
