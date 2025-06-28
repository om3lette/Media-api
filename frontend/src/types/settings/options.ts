import type {
  AudioCodecs,
  AudioBitrates,
  AudioSampleRates,
  VideoFPS,
  VideoPresets,
  VideoCodecs,
  TranscriptionLanguages
} from "./base";

export interface AudioSettingsOptions {
  codec: AudioCodecs;
  bitrate: AudioBitrates;
  sampleRate: AudioSampleRates;
}

export interface FfmpegSettings {}

export interface FfmpegSettingsOptions {
  preset: string[];
  video: {
    presets: VideoPresets;
    fps: VideoFPS;
    audioBitrate: AudioBitrates;
    audioSampleRate: AudioSampleRates;
  };
  codecs: {
    video: VideoCodecs;
    audio: AudioCodecs;
  };
}

export interface TranscriptionSettingsOptions {
  language: TranscriptionLanguages;
}

export interface SettingsOptions {
  audio: AudioSettingsOptions;
  ffmpeg: FfmpegSettingsOptions;
  transcription: TranscriptionSettingsOptions;
}
