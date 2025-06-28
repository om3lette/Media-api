import type { WindowSize } from "@/types/types";
import { useWindowSize } from "@vueuse/core";
import { computed } from "vue";

const { width } = useWindowSize();

export const useSize = () => {
  const windowSize = computed<WindowSize>(() => {
    // Media query values with adjusted sm and extra
    // category for xs devices e.g iPhone SE
    // xs <= 420px
    // 420px < small < 768px
    if (width.value <= 420) return "xs";
    if (width.value < 768) return "sm";
    if (width.value < 1024) return "md";
    if (width.value < 1280) return "lg";
    if (width.value < 1536) return "xl";
    return "2xl";
  });
  return { windowSize };
};
