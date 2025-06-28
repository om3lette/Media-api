<script setup lang="ts">
import InputCard from "../InputCard.vue";
import OperationButton from "./OperationButton.vue";
import { useI18n } from "vue-i18n";
import Button from "primevue/button";
import { inject, toRef } from "vue";
import type { Ref } from "vue";
import type { Operations } from "@/types/types";

const { t } = useI18n();

defineModel<boolean>("button-loading");
const props = defineProps<{ enableProcessButton: boolean }>();
const emit = defineEmits<{
  submit: [];
}>();

const enableProcessButton = toRef(props, "enableProcessButton");

const operations = inject<Ref<Operations>>("availableOperations")!;
const operationIcons: Map<string, string> = new Map([
  ["compress", "video"],
  ["extract-audio", "headphones"],
  ["transcribe", "book"],
  ["summarize", "chart-bar"]
]);

const getIconByName = (name: string) => {
  return operationIcons.get(name) || "question-circle";
};
</script>

<template>
  <InputCard
    title-selector="process.operations.title"
    description-selector="process.operations.description"
  >
    <template #body>
      <div class="flex flex-col justify-between h-full">
        <div class="grid grid-cols-1 p-4 xl:grid-cols-2 xl:grid-rows-2 xl:p-7 gap-4 flex-auto">
          <OperationButton
            v-for="operation in operations"
            :key="`operation-${operation}`"
            :icon="getIconByName(operation)"
            :type="operation"
          />
        </div>
        <div class="w-full">
          <Button
            @click="emit('submit')"
            :loading="buttonLoading"
            :disabled="!enableProcessButton || buttonLoading"
            class="w-full p-6 hover:cursor-pointer hover:bg-gray-800 transition-colors duration-200 disabled:pointer-events-none disabled:bg-gray-500 space-x-2 bg-black text-white"
            icon="pi pi-file-edit"
            severity="contrast"
            unstyled
            :label="t('process.operations.start')"
          />
        </div>
      </div>
    </template>
  </InputCard>
</template>
