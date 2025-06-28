from backend.src.config.enums import AudioCodecs, VideoCodecs


def get_suffix_by_video_codec(codec: VideoCodecs):
    if codec in [VideoCodecs.H264, VideoCodecs.H265]:
        return "mp4"
    raise NameError(f"No suffix specified for codec: {codec}")


def get_suffix_by_audio_codec(codec: AudioCodecs):
    if codec in [AudioCodecs.MP3]:
        return "mp3"
    if codec in [AudioCodecs.AAC]:
        return "m4a"
    raise NameError(f"No suffix specified for codec: {codec}")
