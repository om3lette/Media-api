<script setup lang="ts">
import { useI18n } from "vue-i18n";
import SourceTypeButton from "@/components/process/sourceInput/SourceTypeButton.vue";
import FileSourceInput from "./inputTypes/FileSourceInput.vue";
import UrlSourceInput from "./inputTypes/UrlSourceInput.vue";
import InputCard from "../InputCard.vue";
import { ref } from "vue";
const { t } = useI18n();

const sourceType = ref<string>("file");
</script>

<template>
  <InputCard
    title-selector="process.source.title"
    description-selector="process.source.description"
  >
    <template #body>
      <div class="flex flex-col h-full">
        <div class="flex border-b-1 border-gray-200">
          <SourceTypeButton
            v-model="sourceType"
            class="w-1/2"
            :text="t('process.source.type.file')"
            icon="upload"
            type="file"
          />
          <SourceTypeButton
            v-model="sourceType"
            class="w-1/2"
            :text="t('process.source.type.url')"
            icon="globe"
            type="url"
          />
        </div>
        <div class="flex-1 p-7 xl:min-h-[33vh]">
          <FileSourceInput v-if="sourceType === 'file'" />
          <UrlSourceInput v-if="sourceType === 'url'" />
        </div>
      </div>
    </template>
  </InputCard>
</template>
