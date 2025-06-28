import { computed, ref } from "vue";
import { defineStore } from "pinia";
import type { Operation, Operations } from "@/types/types";

export const useOperationsStore = defineStore("operations", () => {
  const selectedOperations = ref<Operations>([]);
  const size = computed<number>(() => selectedOperations.value.length);

  function addOperation(operation: Operation) {
    selectedOperations.value.push(operation);
  }

  function deleteOperation(operation: Operation) {
    selectedOperations.value = selectedOperations.value.filter((cur) => cur !== operation);
  }

  function has(operation: Operation) {
    return selectedOperations.value.includes(operation);
  }

  function $reset() {
    selectedOperations.value = [];
  }

  return { selectedOperations, size, addOperation, deleteOperation, has, $reset };
});
