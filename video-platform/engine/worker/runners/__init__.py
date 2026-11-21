"""Model runners. Each one turns a job spec from the engine into the argv of the model's own,
documented inference command. Nothing here imports a model: the command runs in that model's
own Python environment, because the models pin incompatible dependency versions."""
from . import wan22, hunyuan15, ltx2, cogvideox, mock

RUNNERS = {"wan22": wan22, "hunyuan15": hunyuan15, "ltx2": ltx2, "cogvideox": cogvideox, "mock": mock}


class RunnerError(Exception):
    def __init__(self, message, retryable=False):
        super().__init__(message)
        self.retryable = retryable
