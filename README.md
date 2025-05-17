# Video utility

Originally made for automatic compression and transcription of lecture footage

## How to run

### Locally

`virtualenv` package is required to proceed. [ffmpeg](https://www.ffmpeg.org/download.html) must also be present\
Note that dependencies for the project exceed 6gb in size, if `/tmp` runs out of space one can create a folder elsewhere and
[specify](https://stackoverflow.com/a/67123076/20957519) `TMPDIR` env for `pip install`.
```bash
git clone https://github.com/om3lette/Simple-ffmpeg-wrapper.git && \
cd Simple-tasks-wrapper && \
python3 -m venv .venv && source .venv/bin/activate && \
pip install -r requirements.txt && \
uvicorn src.api.main:app --host 0.0.0.0 --port 8081
```

### Docker

There are two main folders that we need to persist: `data` and `out`.
- `data` stores "raw" files,
- `out` stores "processed" files

For transcription `openai-whisper` module is used. It stores the models pulled by `load_module` in `.cache` directory
of the given user. It can be ignored, but it will result in downloading the model every time the app is started.\
Port `3000` can be freely changed
```bash
docker build https://github.com/om3lette/Simple-ffmpeg-wrapper.git -t render-pipeline && \
docker run --rm -p 3000:8000 --name render \
  -v <YOUR_PREFERED_PATH>/pipeline/data:/render-app/data \
  -v <YOUR_PREFERED_PATH>/pipeline/out:/render-app/out \
  -v <YOUR_PREFERED_PATH>/pipeline/whisper:/root/.cache/whisper \
  render-pipeline
```
