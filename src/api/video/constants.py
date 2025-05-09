MAX_REQUESTS_BACKLOG: int = 5
REQUEST_QUEUE_RETRIEVAL_INTERVAL: float = 0.5 # Time in seconds

# Do not set as mp4 as ffmpeg won't allow to use the codec specified
OUT_FILE_EXTENSION: str = "mp4"
OUT_AUDIO_FILE_EXTENSION: str = "mp3"
OUT_TRANSCRIPTION_FILE_EXTENSION: str = "txt"
OUT_SUMMARY_FILE_EXTENSION: str = "md"

INPUT_FILENAME: str = "raw"
OUT_FILENAME: str = "out"
AUDIO_FILENAME: str = "audio"
TRANSCRIPTION_FILENAME: str = "transcription"
SUMMARY_FILENAME: str = "summary"
