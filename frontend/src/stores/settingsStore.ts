import { defineStore } from "pinia";
import { ref } from "vue";
import {
  type AudioSettings,
  type FfmpegSettings,
  type TranscribeSettings
} from "@/types/settings/request";
import { type VideoPreset } from "@/types/settings/base";
export const useSettingsStore = defineStore("settings", () => {
  const transcribe = ref<TranscribeSettings>({ language: "none" });
  const audio = ref<AudioSettings>({ codec: "libmp3lame", bitrate: 320, sampleRate: 44100 });
  const ffmpeg = ref<FfmpegSettings>({
    preset: "Veryfast",
    video: {
      width: 1920,
      height: 1080,
      videoBitrate: 2500,
      audioBitrate: 320,
      audioSampleRate: 44100,
      fps: 30
    },
    codecs: { video: "libx264", audio: "libmp3lame" }
  });

  const updateResolution = (resolution: VideoPreset) => {
    if (resolution[0] <= 640 || resolution[1] <= 360) return;
    ffmpeg.value.video.width = resolution[0];
    ffmpeg.value.video.height = resolution[1];
  };

  function $reset() {
    transcribe.value = { language: "none" };
    audio.value = { codec: "libmp3lame", bitrate: 320, sampleRate: 44100 };
    ffmpeg.value = {
      preset: "Veryfast",
      video: {
        width: 1920,
        height: 1080,
        videoBitrate: 2500,
        audioBitrate: 320,
        audioSampleRate: 44100,
        fps: 30
      },
      codecs: { video: "libx264", audio: "libmp3lame" }
    };
  }
  return { transcribe, audio, ffmpeg, updateResolution, $reset };
});
