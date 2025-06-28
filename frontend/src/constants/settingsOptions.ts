import {
  FfmpegPresets,
  type AudioBitrates,
  type AudioCodecs,
  type AudioSampleRates,
  type TranscriptionLanguages,
  type VideoCodecs,
  type VideoFPS,
  type VideoPresets
} from "@/types/settings/base";
import { type SettingsOptions } from "@/types/settings/options";

const audioSampleRates: AudioSampleRates = [16000, 44100, 48000, 96000];
const audioBitrates: AudioBitrates = [64, 96, 128, 192, 256, 320];
const audioCodecs: AudioCodecs = [
  {
    label: "MP3 (LAME)",
    value: "libmp3lame"
  },
  {
    label: "AAC",
    value: "aac"
  }
];

const videoPresets: VideoPresets = [
  [3840, 2160, "4K"],
  [2560, 1440, "2K"],
  [1920, 1080, "Full HD"],
  [1280, 720, "HD"],
  [854, 480, "SD"],
  [640, 360, "360p"]
];
const videoCodecs: VideoCodecs = [
  {
    label: "H.264",
    value: "libx264"
  },
  {
    label: "H.265",
    value: "libx265"
  }
];
const videoFPS: VideoFPS = [120, 60, 30, 25, 24];

const ffmpegPresets: string[] = Object.keys(FfmpegPresets);

const transctiptionLanguages: TranscriptionLanguages = [
  {
    label: "Русский",
    value: "ru"
  },
  {
    label: "English",
    value: "en"
  },
  {
    label: "Auto",
    value: "none"
  }
];

export const settingsOptions: SettingsOptions = {
  audio: {
    codec: audioCodecs,
    bitrate: audioBitrates,
    sampleRate: audioSampleRates
  },
  ffmpeg: {
    preset: ffmpegPresets,
    video: {
      presets: videoPresets,
      fps: videoFPS,
      audioBitrate: audioBitrates,
      audioSampleRate: audioSampleRates
    },
    codecs: {
      video: videoCodecs,
      audio: audioCodecs
    }
  },
  transcription: {
    language: transctiptionLanguages
  }
};
