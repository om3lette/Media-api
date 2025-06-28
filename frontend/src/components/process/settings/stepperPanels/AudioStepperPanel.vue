<script setup lang="ts">
import type { SettingsOptions } from "@/types/settings/options";
import Select from "primevue/select";
import GridWrapper from "./GridWrapper.vue";
import InputWrapper from "./InputWrapper.vue";
import { inject, ref, watch } from "vue";
import { useSettingsStore } from "@/stores/settingsStore";

const settingsOptions = inject<SettingsOptions>("settingsOptions")!;
const audioBitrateOptions = settingsOptions.audio.bitrate.map((bitrate) => {
  return { value: bitrate, label: `${bitrate} kbps` };
});
const audioSampleRateOptions = settingsOptions.audio.sampleRate.map((sampleRate) => {
  return { value: sampleRate, label: `${sampleRate} Hz` };
});

const props = defineProps<{ writeVideoSettings?: boolean; enableDivider?: boolean }>();
const settingsStore = useSettingsStore();
const sampleRate = ref<number>(settingsStore.audio.sampleRate);

watch(sampleRate, () => {
  if (props.writeVideoSettings) settingsStore.ffmpeg.video.audioSampleRate = sampleRate.value;
  else settingsStore.audio.sampleRate = sampleRate.value;
});
const bitrate = ref<number>(settingsStore.audio.bitrate);
watch(bitrate, () => {
  if (props.writeVideoSettings) settingsStore.ffmpeg.video.audioBitrate = bitrate.value;
  else settingsStore.audio.bitrate = bitrate.value;
});

const codec = ref<string>(settingsStore.audio.codec);
watch(codec, () => {
  if (props.writeVideoSettings) settingsStore.ffmpeg.codecs.audio = codec.value;
  else settingsStore.audio.codec = codec.value;
});
</script>

<template>
  <GridWrapper t-title="audio.title" :divired="enableDivider ?? false">
    <template #body>
      <InputWrapper id="audio-codec-input" t-selector="audio.codec">
        <Select
          id="audio-codec-input"
          v-model="codec"
          :options="settingsOptions.ffmpeg.codecs.audio"
          option-label="label"
          option-value="value"
        />
      </InputWrapper>
      <InputWrapper id="audio-bitrate-input" t-selector="audio.bitrate">
        <Select
          id="audio-bitrate-input"
          v-model="bitrate"
          :options="audioBitrateOptions"
          option-label="label"
          option-value="value"
        />
      </InputWrapper>
      <InputWrapper id="audio-samplerate-input" t-selector="audio.samplerate">
        <Select
          id="audio-samplerate-input"
          v-model="sampleRate"
          :options="audioSampleRateOptions"
          option-label="label"
          option-value="value"
        />
      </InputWrapper>
    </template>
  </GridWrapper>
</template>
