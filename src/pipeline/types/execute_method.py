from typing import Union

from src.pipeline.types.preprocessor import Preprocessor
from src.pipeline.types.job import Job
from src.pipeline.types.postprocessor import Postprocessor

ExecuteMethod = Union[Preprocessor, Job, Postprocessor]
