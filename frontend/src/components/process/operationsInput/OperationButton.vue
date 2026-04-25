<script setup lang="ts">
import { useI18n } from "vue-i18n";
import Message from "primevue/message";
import { ref, computed } from "vue";
import { useOperationsStore } from "@/stores/operationsStore";
import emitter from "@/plugins/emitter";

const operationsStore = useOperationsStore();
const props = defineProps<{ type: string; icon: string }>();

const { t } = useI18n();
const iconClass: string = `pi-${props.icon}`;
const isSelected = ref<boolean>(false);
const iconColor = computed<string>(() => (isSelected.value ? "white" : "black"));

emitter.on("process-request-sent", () => {
  isSelected.value = false;
});

const onSelected = () => {
  isSelected.value = !isSelected.value;
  if (isSelected.value) {
    operationsStore.addOperation(props.type);
  } else {
    operationsStore.deleteOperation(props.type);
  }
};
</script>

<template>
  <div
    @click="onSelected"
    :class="{ 'border-surface-700 bg-surface-100 dark:border-surface-400 dark:bg-surface-500 ': isSelected, 'border-surface-200 dark:border-surface-600': !isSelected }"
    class="transition-[background-color] duration-200 ease-linear hover:cursor-pointer hover:bg-surface-200 dark:hover:bg-surface-600 rounded-md border-3 select-none p-4 flex items-center space-x-3"
  >
    <div
      :class="{ 'border-surface-700 bg-surface-700 dark:border-surface-400 dark:bg-surface-400': isSelected, 'border-surface-300 bg-surface-100 dark:border-surface-700 dark:bg-surface-600': !isSelected }"
      class="border py-2 px-3 rounded-full"
    >
      <i :class="iconClass" class="pi" :style="{ color: iconColor }"></i>
    </div>
    <div class="flex flex-col">
      <div>{{ t(`process.operations.types.${type}.title`) }}</div>
      <Message size="small" severity="secondary" variant="simple">{{
        t(`process.operations.types.${type}.description`)
      }}</Message>
    </div>
  </div>
</template>
