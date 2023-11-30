from typing import Optional

from clearaml.validation.base import TrainValidIterator


class MLAlgo:

    def init_params_on_input(self, train_valid_iterator: Optional[TrainValidIterator] = None):
        pass
