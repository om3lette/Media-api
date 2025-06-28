<script setup lang="ts">
import { useI18n } from "vue-i18n";

defineProps<{
  icon: string;
  tTitle?: string;
  title?: string;
  tDescription?: string;
  description?: string;
}>();
const { t } = useI18n();
</script>

<template>
  <div class="flex flex-col justify-center space-y-4 items-center h-full">
    <div class="flex justify-center border-1 bg-white p-6 border-gray-400 rounded-full">
      <i style="font-size: 2rem; color: #708090" :class="`pi pi-${icon}`"></i>
    </div>
    <div class="flex flex-col">
      <p class="text-center mb-1">{{ title ?? t("process.source.selection.title") }}</p>
      <small class="text-center text-gray-500">{{
        description ?? t("process.source.selection.formats")
      }}</small>
    </div>
    <div>
      <slot name="footer"></slot>
    </div>
  </div>
</template>
