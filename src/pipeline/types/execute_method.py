from typing import Union

from src.pipeline.types.job import Job
from src.pipeline.types.postprocessor import Postprocessor
from src.pipeline.types.preprocessor import Preprocessor

ExecuteMethod = Union[Preprocessor, Job, Postprocessor]
