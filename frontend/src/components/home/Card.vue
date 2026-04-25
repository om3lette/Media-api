<script setup lang="ts">
import Card from "primevue/card"
import { useI18n } from "vue-i18n";

defineProps<{ icon: string; cardNameSelector: string; color: string }>();
const { t } = useI18n();
</script>

<template>
  <Card
    class="rounded-lg shadow-sm bg-surface-0 border-2 border-surface-200 hover:shadow-lg transition-shadow"
  >
    <template #title>
      <div class="flex flex-col space-y-1.5 p-6 text-center pb-4">
        <div
          class="mx-auto aspect-square rounded-full flex bg-surface-100 dark:bg-surface-700 items-center justify-center mb-4"
        >
          <i :class="`pi-${icon}`" class="text-4xl! pi p-5"></i>
        </div>
        <h3 class="font-semibold tracking-tight text-2xl">
          {{ t(`home.cards.${cardNameSelector}.title`) }}
        </h3>
        <p class="text-surface-500 dark:text-surface-400 text-base">
          {{ t(`home.cards.${cardNameSelector}.description`) }}
        </p>
      </div>
    </template>
    <template #content>
      <div class="p-6 pt-0">
        <div class="space-y-4">
          <slot name="body"></slot>
        </div>
      </div>
    </template>
  </Card>
</template>
