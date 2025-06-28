export interface AudioSettings {
  codec: string;
  bitrate: number;
  sampleRate: number;
}

export interface FfmpegSettings {
  preset: string;
  video: {
    width: number;
    height: number;
    videoBitrate: number;
    audioBitrate: number;
    audioSampleRate: number;
    fps: number;
  };
  codecs: {
    video: string;
    audio: string;
  };
}

export interface TranscribeSettings {
  language: string;
}

export interface Settings {
  audio: AudioSettings;
  ffmpeg: FfmpegSettings;
  transcription: TranscribeSettings;
}
