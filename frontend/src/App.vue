<script setup lang="ts">
import GlobalHeader from "./components/common/GlobalHeader.vue";
import GlobalFooter from "./components/common/GlobalFooter.vue";
</script>

<template>
  <div class="flex flex-col min-h-screen">
    <GlobalHeader v-if="$route.path !== '/process/'" />
    <main class="flex-1">
      <RouterView />
    </main>
    <GlobalFooter />
  </div>
</template>
