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
    :class="{ 'border-black bg-gray-100': isSelected, 'border-gray-200': !isSelected }"
    class="transition-[background-color] duration-200 ease-linear hover:cursor-pointer hover:bg-gray-200 rounded-md border-3 select-none p-4 flex items-center space-x-6"
  >
    <div
      :class="{ 'border-black bg-black': isSelected, 'border-gray-300 bg-gray-50': !isSelected }"
      class="border-1 py-2 px-3 rounded-full"
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
