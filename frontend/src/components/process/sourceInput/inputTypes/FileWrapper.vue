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
    <div class="flex justify-center border bg-surface-0 p-6 border-surface-400 dark:bg-surface-500 rounded-full">
      <i :class="['pi', `pi-${icon}`, 'text-surface-500', 'dark:text-surface-300']" style="font-size: 2rem"></i>
    </div>
    <div class="flex flex-col">
      <p class="text-center mb-1">{{ title ?? t("process.source.selection.title") }}</p>
       <small class="text-center text-surface-500 dark:text-surface-400 ">{{
        description ?? t("process.source.selection.formats")
      }}</small> 
    </div>
    <div>
      <slot name="footer"></slot>
    </div>
  </div>
</template>
