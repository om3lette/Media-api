from typing import Union

from backend.src.pipeline.types.job import Job
from backend.src.pipeline.types.postprocessor import Postprocessor
from backend.src.pipeline.types.preprocessor import Preprocessor

ExecuteMethod = Union[Preprocessor, Job, Postprocessor]
