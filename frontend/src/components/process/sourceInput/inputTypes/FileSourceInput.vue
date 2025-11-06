<script setup lang="ts">
import { ref } from "vue";
import { MAX_FILESIZE } from "@/constants/file";
import FileWrapper from "./FileWrapper.vue";
import Message from "primevue/message";
import { useI18n } from "vue-i18n";
import { useSourceStore } from "@/stores/sourceStore";
import emitter from "@/plugins/emitter";
import toastWrapper from "@/plugins/toastWrapper";
import { fileSizeToString } from "@/utils";
import { onMounted } from "vue";

const sourceStore = useSourceStore();

const fileUploaded = ref<boolean>(false);
const fileSizeString = ref<string>("");
const filename = ref<string>("");
const { t } = useI18n();

emitter.on("process-request-sent", () => {
  filename.value = "";
  fileSizeString.value = "";
  fileUploaded.value = false;
});

let fileInput: HTMLInputElement;
onMounted(() => {
  fileInput = document.getElementById("source-file-input") as HTMLInputElement;
});

const validateCondition = (
  errorCondition: CallableFunction,
  errorSelector: string,
  tArgs: Record<string, string> = {}
): Boolean => {
  if (!errorCondition()) return false;
  fileInput.value = "";
  toastWrapper.error(t(errorSelector, tArgs));
  return true;
};

const onFileInput = (e: Event) => {
  let files: FileList | null = (e.target as HTMLInputElement).files;

  const filesNotFoundError = validateCondition(
    () => !files || files.length < 1,
    "process.errors.file-not-found"
  );
  if (filesNotFoundError) return;

  files = files as FileList;
  const filesizeError: Boolean = validateCondition(
    () => files[0]!.size > MAX_FILESIZE,
    "process.errors.file-size-exceeded",
    {
      maxSize: `${fileSizeToString(MAX_FILESIZE)}`
    }
  );
  if (filesizeError) return;

  const file = files[0]!;
  fileSizeString.value = fileSizeToString(file.size);

  sourceStore.setFile(file);
  filename.value = file.name;
  fileUploaded.value = true;
};
</script>

<template>
  <label v-if="!fileUploaded" for="source-file-input" class="h-full block">
    <div
      class="py-5 h-full rounded-md border-2 border-gray-300 border-dashed bg-gray-50 hover:cursor-pointer hover:bg-gray-100 ease-out duration-200 transition-colors"
    >
      <input
        @input="onFileInput"
        type="file"
        id="source-file-input"
        style="display: none"
        accept=".mp4, .avi, .wnv, .mkv, .mov, .m4a, .mp3, .wav, .flac, .aiff"
      />
      <FileWrapper
        icon="upload"
        t-title="process.source.selection.title"
        t-description="process.source.selection.formats"
      />
    </div>
  </label>
  <div v-else class="py-5 h-full rounded-md bg-gray-50">
    <FileWrapper icon="file" :title="filename" :description="fileSizeString">
      <template #footer>
        <label class="hover:cursor-pointer" for="change-source-file-input">
          <button class="pointer-events-none border-1 border-gray-300 rounded-md bg-white p-2">
            <Message severity="contrast" variant="simple" size="small">{{
              t("process.source.selection.change-file")
            }}</Message>
          </button>
        </label>
        <input
          @input="onFileInput"
          type="file"
          id="change-source-file-input"
          style="display: none"
          accept=".mp4, .avi, .wnv, .mkv, .mov, .m4a, .mp3, .wav, .flac, .aiff"
        />
      </template>
    </FileWrapper>
  </div>
</template>
