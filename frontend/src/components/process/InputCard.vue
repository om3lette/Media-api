<script setup lang="ts">
import { useI18n } from "vue-i18n";

defineProps<{ titleSelector: string; descriptionSelector: string }>();
const { t } = useI18n();
</script>

<template>
  <div class="flex flex-col border-3 border-gray-200 rounded-md overflow-hidden">
    <div class="p-4 border-b-1 border-gray-200 bg-gray-50">
      <h2>{{ t(titleSelector) }}</h2>
      <small class="text-gray-500">{{ t(descriptionSelector) }}</small>
    </div>
    <div class="h-full relative bg-white">
      <slot name="body"></slot>
    </div>
  </div>
</template>
