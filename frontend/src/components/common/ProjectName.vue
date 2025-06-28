<script setup lang="ts">
import { PROJECT_NAME } from "@/constants/project";
</script>

<template>
  <RouterLink to="/">
    <div class="text-xl font-semibold">{{ PROJECT_NAME }}</div>
  </RouterLink>
</template>
