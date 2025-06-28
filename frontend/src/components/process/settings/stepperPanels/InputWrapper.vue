<script setup lang="ts">
import { useI18n } from "vue-i18n";

const { t } = useI18n();
const props = defineProps<{ id: string; tSelector: string }>();
</script>

<template>
  <div class="flex flex-col space-y-1">
    <label :for="id">{{ t(`process.settings.inputs.${props.tSelector}`) }}</label>
    <slot></slot>
  </div>
</template>
