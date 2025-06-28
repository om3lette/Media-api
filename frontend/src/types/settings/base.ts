export type AudioSampleRates = number[];
export type AudioBitrates = number[];

interface LabelValueObject {
  label: string;
  value: string;
}

export interface AudioCodec extends LabelValueObject {}
export type AudioCodecs = AudioCodec[];

export type VideoPreset = [number, number, string];
export type VideoPresets = VideoPreset[];

export interface VideoCodec extends LabelValueObject {}
export type VideoCodecs = VideoCodec[];
export type VideoFPS = number[];

export interface TranscriptionLanguage extends LabelValueObject {}
export type TranscriptionLanguages = TranscriptionLanguage[];

export enum FfmpegPresets {
  Ultrafast = "ultrafast",
  Veryfast = "veryfast",
  Faster = "faster",
  Fast = "fast",
  Medium = "medium",
  Slow = "slow",
  Slower = "slower",
  Veryslow = "veryslow"
}
