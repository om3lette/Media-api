<script setup lang="ts">
import { useI18n } from "vue-i18n";
import { Button } from "primevue";
import Card from "@/components/home/Card.vue";
import CardPoint from "@/components/home/CardPoint.vue";
const { t } = useI18n();
</script>

<template>
  <main class="flex justify-center my-10 bg-gray-50">
    <div class="w-11/12 2xl:w-9/12 space-y-8 flex flex-col items-center">
      <div class="mt-10 w-5/6 xl:w-2/3 flex flex-col justify-center items-center space-y-8">
        <h1 class="text-center !text-4xl lg:!text-5xl">{{ t("home.process-files") }}</h1>
        <p class="text-xl text-center xl:max-w-[45vw]">{{ t("home.description") }}</p>
        <RouterLink to="/process/">
          <Button
            class="!px-10 !py-3"
            severity="contrast"
            icon-pos="right"
            icon="pi pi-arrow-right"
            :label="t('home.start')"
          />
        </RouterLink>
      </div>
      <div class="mt-20 w-full">
        <h2 class="text-center mb-12">{{ t("home.what-you-can-do") }}</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
          <Card icon="file" card-name-selector="media" class="min-w-1/2" color="blue">
            <template #header> </template>
            <template #body>
              <CardPoint icon="video" card-name="media" point-name="compress" />
              <CardPoint icon="headphones" card-name="media" point-name="extract-audio" />
              <CardPoint icon="book" card-name="media" point-name="transcribe" />
              <CardPoint icon="chart-bar" card-name="media" point-name="summary" />
            </template>
          </Card>
          <Card icon="file-pdf" card-name-selector="files" class="min-w-1/2" color="green">
            <template #header> </template>
            <template #body> </template>
          </Card>
        </div>
      </div>
      <div class="text-center">
        <div
          class="rounded-lg border border-gray-300 shadow-sm max-w-2xl mx-auto bg-gradient-to-r from-[#E8E8E8] from-25%"
        >
          <div class="p-6 py-8">
            <h3 class="text-2xl font-bold mb-4">{{ t("home.ready-to-start") }}</h3>
            <p class="text-gray-600 mb-6">
              {{ t("home.process-files-2") }}
            </p>
            <RouterLink to="/process/">
              <Button icon="pi pi-upload" severity="contrast" :label="t('home.start')"></Button>
            </RouterLink>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<style>
body {
  background-color: #f9fafb !important;
}
</style>
