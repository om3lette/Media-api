<script setup lang="ts">
import { computed } from "vue";

const props = defineProps<{ text: string; icon: string; type: string }>();
const sourceTypeModel = defineModel<string>();
const iconClass: string = `pi-${props.icon}`;

const isSelected = computed<boolean>(() => sourceTypeModel.value === props.type);
</script>

<template>
  <div
    @click="() => (sourceTypeModel = type)"
    :class="{ 'border-b-2 bg-gray-50': isSelected }"
    class="transition-colors ease-out duration-200 hover:cursor-pointer hover:bg-gray-100 flex justify-center p-5"
  >
    <div class="flex items-center space-x-4">
      <span class="pi" :class="iconClass"></span>
      <span>{{ text }}</span>
    </div>
  </div>
</template>
