<script setup lang="ts">
import { useI18n } from "vue-i18n";

defineProps<{ icon: string; cardName: string; pointName: string }>();
const { t } = useI18n();
</script>

<template>
  <div class="flex items-center space-x-3">
    <i :class="`pi pi-${icon}`"></i>
    <span>{{ t(`home.cards.${cardName}.points.${pointName}`) }}</span>
  </div>
</template>
