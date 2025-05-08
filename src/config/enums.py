from enum import StrEnum

class FfmpegPresets(StrEnum):
	ULTRAFAST = "ultrafast"
	SUPERFAST = "superfast"
	VERYFAST = "veryfast"
	FASTER = "faster"
	MEDIUM = "medium"
	SLOW = "slow"
	SLOWER = "slower"
	VERYSLOW = "veryslow"

class VideoCodecs(StrEnum):
	H264 = "libx264"
	H265 = "libx265"

class AudioCodecs(StrEnum):
	MP3 = "libmp3lame"
	AAC = "aac"
