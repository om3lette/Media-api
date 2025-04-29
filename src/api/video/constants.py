MAX_REQUESTS_BACKLOG: int = 5
REQUEST_QUEUE_RETRIEVAL_INTERVAL: float = 0.5 # Time in seconds

# Do not set as mp4 as ffmpeg won't allow to use the codec specified
OUT_FILE_EXTENSION: str = "mov"
INPUT_FILENAME: str = "raw"
OUT_FILENAME: str = "out"
