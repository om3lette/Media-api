<script setup>
import ProjectName from "@/components/common/ProjectName.vue";
import { useI18n } from "vue-i18n";
import { Button } from "primevue";

const { t } = useI18n();
</script>

<template>
  <header
    class="z-100 sticky backdrop-blur-sm top-0 w-full flex justify-around py-4 bg-white/80 border-1 border-gray-200 !border-t-0"
  >
    <div class="w-11/12 2xl:w-9/12 flex justify-between">
      <div class="flex items-center space-x-2">
        <img class="w-[24px] aspect-square" src="/icons/flash.png" />
        <ProjectName />
      </div>
      <nav>
        <RouterLink v-if="$route.path === '/'" to="/process/">
          <Button severity="secondary" outlined :label="t('common.get-started')"></Button>
        </RouterLink>
        <RouterLink v-else to="/">
          <Button severity="secondary" outlined :label="t('common.get-started')"></Button>
        </RouterLink>
      </nav>
    </div>
  </header>
</template>
