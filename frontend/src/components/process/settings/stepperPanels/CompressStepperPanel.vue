<script setup lang="ts">
import type { SettingsOptions } from "@/types/settings/options";
import Select from "primevue/select";
import AudioStepperPanel from "./AudioStepperPanel.vue";
import GridWrapper from "./GridWrapper.vue";
import InputNumber from "primevue/inputnumber";
import InputWrapper from "./InputWrapper.vue";
import { useSettingsStore } from "@/stores/settingsStore";
import type { VideoPreset } from "@/types/settings/base";
import { inject, ref, watchEffect } from "vue";

const settingsStore = useSettingsStore();
const settingsOptions = inject<SettingsOptions>("settingsOptions")!;
const videoPresetOptions = settingsOptions.ffmpeg.video.presets.map((preset) => {
  return { value: preset, label: `${preset[2]} (${preset[0]}x${preset[1]})` };
});
const videoFpsOptions = settingsOptions.ffmpeg.video.fps.map((fps) => {
  return { value: fps, label: `${fps} FPS` };
});

const selectedVideoResolution = ref<VideoPreset>(
  settingsOptions.ffmpeg.video.presets.find((x) => x[0] == 1920) ?? [0, 0, "Loading..."]
);
watchEffect(() => {
  settingsStore.updateResolution(selectedVideoResolution.value);
});
</script>

<template>
  <GridWrapper t-title="video.title">
    <template #body>
      <InputWrapper id="video-codec-input" t-selector="video.codec">
        <Select
          id="video-codec-input"
          v-model="settingsStore.ffmpeg.codecs.video"
          :options="settingsOptions.ffmpeg.codecs.video"
          option-label="label"
          option-value="value"
        />
      </InputWrapper>
      <InputWrapper id="video-bitrate-input" t-selector="video.bitrate">
        <InputNumber
          v-model="settingsStore.ffmpeg.video.videoBitrate"
          id="video-bitrate-input"
          showButtons
          fluid
        />
      </InputWrapper>
      <InputWrapper id="video-encoding-input" t-selector="video.encoding-preset">
        <Select
          v-model="settingsStore.ffmpeg.preset"
          :default-value="settingsStore.ffmpeg.preset"
          id="video-encoding-input"
          :options="settingsOptions.ffmpeg.preset"
        />
      </InputWrapper>
      <InputWrapper id="video-resolution-input" t-selector="video.resolution">
        <Select
          id="video-resolution-input"
          v-model="selectedVideoResolution"
          :options="videoPresetOptions"
          option-label="label"
          option-value="value"
        />
      </InputWrapper>
      <InputWrapper id="video-framerate-input" t-selector="video.framerate">
        <Select
          id="video-framerate-input"
          v-model="settingsStore.ffmpeg.video.fps"
          :options="videoFpsOptions"
          option-label="label"
          option-value="value"
        />
      </InputWrapper>
    </template>
  </GridWrapper>
  <AudioStepperPanel :write-video-settings="true" :enable-divider="true" />
</template>
