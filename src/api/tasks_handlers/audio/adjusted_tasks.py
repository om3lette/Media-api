from src.pipeline.tasks.jobs import TranscribeTask
from src.pipeline.tasks.postprocessors import SummarizeTask

audio_transcribe_task: TranscribeTask = TranscribeTask(dependencies=[])
audio_summarize_task: SummarizeTask = SummarizeTask(
    dependencies=[audio_transcribe_task]
)
