<script setup lang="ts">
import { useI18n } from "vue-i18n";

defineProps<{ icon: string; cardNameSelector: string; color: string }>();
const { t } = useI18n();
</script>

<template>
  <div
    class="rounded-lg shadow-sm bg-white border-2 border-gray-200 hover:shadow-lg transition-shadow"
  >
    <div class="flex flex-col space-y-1.5 p-6 text-center pb-4">
      <div
        class="mx-auto aspect-square rounded-full flex bg-gray-100 items-center justify-center mb-4"
      >
        <i :class="`pi-${icon}`" class="!text-4xl pi p-5"></i>
      </div>
      <h3 class="font-semibold tracking-tight text-2xl">
        {{ t(`home.cards.${cardNameSelector}.title`) }}
      </h3>
      <p class="text-muted-foreground text-base">
        {{ t(`home.cards.${cardNameSelector}.description`) }}
      </p>
    </div>
    <div class="p-6 pt-0">
      <div class="space-y-4">
        <slot name="body"></slot>
      </div>
    </div>
  </div>
</template>
