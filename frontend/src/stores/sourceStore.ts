import { ref } from "vue";
import { defineStore } from "pinia";

export const useSourceStore = defineStore("source", () => {
  const url = ref<string>("");
  const file = ref<File>();

  function setUrl(newUrl: string) {
    url.value = newUrl;
  }

  function setFile(newFile: File) {
    file.value = newFile;
  }

  function isSourceSet(): boolean {
    return url.value !== "" || file.value != null;
  }

  function $reset() {
    url.value = "";
    file.value = undefined;
  }

  return { url, file, setUrl, setFile, isSourceSet, $reset };
});
