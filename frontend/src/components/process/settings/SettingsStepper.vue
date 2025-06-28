<script setup lang="ts">
import type { Operations } from "@/types/types";
import SelectButton from "primevue/selectbutton";
import Stepper from "primevue/stepper";
import StepList from "primevue/steplist";
import StepPanel from "primevue/steppanel";
import StepPanels from "primevue/steppanels";

import AudioStepperPanel from "./stepperPanels/AudioStepperPanel.vue";
import CompressStepperPanel from "@/components/process/settings/stepperPanels/CompressStepperPanel.vue";
import TranscriptionStepperPanel from "./stepperPanels/TranscriptionStepperPanel.vue";
import SummarizeStepperPanel from "./stepperPanels/SummarizeStepperPanel.vue";

import { ref, watchEffect, inject, computed } from "vue";
import { useI18n } from "vue-i18n";
import { useOperationsStore } from "@/stores/operationsStore";
import type { Ref } from "vue";
const { t } = useI18n();
const defaultStep: string = "no-operation-selected";

const operationsStore = useOperationsStore();
//const { selectedOperations } = storeToRefs(operationsStore);

const operations = inject<Ref<Operations>>("availableOperations", ref([]));
const activeStep = ref<string>(defaultStep);
const operationOptions = computed(() =>
  operations.value.map((op) => ({
    label: t(`process.operations.types.${op}.title`),
    value: op,
    disabled: !operationsStore.has(op)
  }))
);
watchEffect(() => {
  if (operationsStore.has(activeStep.value)) return;
  if (operationsStore.size !== 0) {
    activeStep.value = operationsStore.selectedOperations[0];
    return;
  }
  activeStep.value = defaultStep;
});
</script>

<template>
  <transition name="resize" appear>
    <div class="w-full space-y-4">
      <SelectButton
        class="stepper-selectbutton !grid !grid-cols-1 xs:!grid-cols-2 md:!flex"
        v-model="activeStep"
        :options="operationOptions"
        optionLabel="label"
        optionValue="value"
        optionDisabled="disabled"
      />
      <transition name="fade">
        <div
          v-show="operationsStore.size > 0"
          class="p-4 border-2 rounded-md border-gray-100 bg-gray-50"
        >
          <Stepper :value="activeStep" class="bg-gray-50">
            <StepList></StepList>
            <StepPanels class="settings-step-pannel">
              <StepPanel value="compress">
                <CompressStepperPanel />
              </StepPanel>
              <StepPanel value="extract-audio">
                <AudioStepperPanel />
              </StepPanel>
              <StepPanel value="transcribe">
                <TranscriptionStepperPanel />
              </StepPanel>
              <StepPanel value="summarize">
                <SummarizeStepperPanel />
              </StepPanel>
            </StepPanels>
          </Stepper>
        </div>
      </transition>
    </div>
  </transition>
</template>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}

.fade-enter-to {
  opacity: 1;
}

.stepper-selectbutton {
  width: 100%;
}
.stepper-selectbutton > button {
  flex: 1 1 0%;
}

.settings-step-pannel > * {
  background-color: oklch(0.984 0.003 247.858) !important;
}
</style>
