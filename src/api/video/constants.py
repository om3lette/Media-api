MAX_REQUESTS_BACKLOG: int = 5
REQUEST_QUEUE_RETRIEVAL_INTERVAL: float = 0.5 # Time in seconds

# Do not set as mp4 as ffmpeg won't allow to use the codec specified
OUT_FILE_EXTENSION: str = "mov"
OUT_AUDIO_FILE_EXTENSION: str = "mp3"
OUT_TRANSCRIPTION_FILE_EXTENSION: str = "txt"

INPUT_FILENAME: str = "raw"
OUT_FILENAME: str = "out"
AUDIO_FILENAME: str = "audio"
TRANSCRIPTION_FILENAME: str = "transcription"
