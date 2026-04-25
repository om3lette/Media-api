<script setup lang="ts">
import { useI18n } from "vue-i18n";

defineProps<{ titleSelector: string; descriptionSelector: string }>();
const { t } = useI18n();
</script>

<template>
  <div class="flex flex-col border-3 border-surface-200 dark:border-surface-600 rounded-md overflow-hidden">
    <div class="p-4 border-b border-surface-200 dark:border-surface-600 bg-surface-100 dark:bg-surface-800">
      <h2>{{ t(titleSelector) }}</h2>
      <small class="text-surface-500">{{ t(descriptionSelector) }}</small>
    </div>
    <div class="h-full relative bg-surface-0 dark:bg-surface-700">
      <slot name="body"></slot>
    </div>
  </div>
</template>
