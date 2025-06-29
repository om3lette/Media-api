<script setup lang="ts">
import { useI18n } from "vue-i18n";
import { PROJECT_NAME } from "@/constants/project";
import ProjectName from "@/components/common/ProjectName.vue";
const { t } = useI18n();
</script>

<template>
  <footer class="w-full flex justify-around py-4 bg-white border-1 border-gray-200 !border-b-0">
    <div
      class="w-11/12 2xl:w-9/12 flex flex-col items-center space-y-3 md:flex-row md:justify-between"
    >
      <div class="flex items-center space-x-2 m-0">
        <img class="w-[24px] aspect-square" src="/icons/flash.png" />
        <ProjectName />
      </div>
      <div class="flex flex-col space-y-1">
        <p class="text-center md:text-left">
          {{ t("common.made-with-love") }}
          <a target="_blank" href="https://github.com/om3lette">om3lette</a>
        </p>
        <small>© 2025 {{ PROJECT_NAME }}. All rights reserved.</small>
      </div>
    </div>
  </footer>
</template>
