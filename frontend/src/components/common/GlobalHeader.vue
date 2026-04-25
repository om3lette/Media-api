<script setup lang="ts">
import { ref } from "vue";
import ProjectName from "@/components/common/ProjectName.vue";
import { useI18n } from "vue-i18n";
import { Select } from "primevue";
import { availableLocales, localeStorageKey } from "@/locales/locales";

const { locale } = useI18n();

const changeLocale = (newLocale: { code: string; name: string }) => {
  locale.value = newLocale.code;
  localStorage.setItem(localeStorageKey, newLocale.code);
};

const selectedLocale = ref(availableLocales.find((l) => l.code === locale.value) || availableLocales[0]);

</script>

<template>
  <header
    class="
    z-100 sticky backdrop-blur-sm top-0 w-full flex justify-around py-4 bg-surface-0 border border-surface-200 border-t-0!
    dark:border-surface-800 dark:bg-surface-800
    "
  >
    <div class="w-11/12 2xl:w-9/12 flex justify-between">
      <div class="flex items-center space-x-2">
        <img class="w-6 aspect-square" src="/icons/flash.png" />
        <ProjectName />
      </div>
      <div class="flex items-center gap-4">
        <Select
          v-model="selectedLocale"
          :options="availableLocales"
          optionLabel="name"
          @change="changeLocale(selectedLocale)"
          aria-label="Select language"
          class="w-32"
        >
          <template #value="slotProps">
            <div class="flex items-center gap-2">
              <i class="pi pi-globe" />
              <span>{{ slotProps.value.name }}</span>
            </div>
          </template>
          <template #option="slotProps">
            <div class="flex items-center gap-2">
              <i class="pi pi-globe" />
              <span>{{ slotProps.option.name }}</span>
            </div>
          </template>
        </Select>
      </div>
    </div>
  </header>
</template>
