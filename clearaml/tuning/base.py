"""Base classes to implement hyperparameter tuning."""

from abc import ABC
from abc import abstractmethod
from typing import Dict
from typing import Optional
from typing import Tuple
from typing import overload

from clearaml.dataset.base import LAMLDataset
from clearaml.validation.base import TrainValidIterator

from clearaml.ml_algo.base import MLAlgo


class DistributionBase(ABC):
    pass


class Choice(DistributionBase):
    def __init__(self, options) -> None:
        self.options = options


class Uniform(DistributionBase):
    def __init__(self, low, high, q=None, log=False) -> None:
        self.low = low
        self.high = high
        self.q = q
        self.log = log


class Normal(DistributionBase):
    def __init__(self, low, high, q=None, log=False) -> None:
        self.low = low
        self.high = high
        self.q = q
        self.log = log


class ParamsTuner(ABC):
    """Base abstract class for hyperparameters tuners."""

    _name: str = "AbstractTuner"
    _best_params: Dict = None
    _fit_on_holdout: bool = False  # if tuner should be fitted on holdout set

    @property
    def best_params(self) -> dict:
        """Get best params.

        Returns:
            Dict with best fitted params.

        Raises:
            AttributeError: If the ParamsTuner has not been fitted yet.

        """
        if not hasattr(self, "_best_params"):
            raise AttributeError("ParamsTuner should be fitted first")
        return self._best_params

    @overload
    def fit(
        self,
        ml_algo: "MLAlgo",
        train_valid_iterator: Optional[TrainValidIterator] = None,
    ) -> Tuple["MLAlgo", LAMLDataset]:
        ...

    @abstractmethod
    def fit(
        self,
        ml_algo: "MLAlgo",
        train_valid_iterator: Optional[TrainValidIterator] = None,
    ) -> Tuple[None, None]:
        """Tune model hyperparameters.

        Args:
            ml_algo: ML algorithm.
            train_valid_iterator: Classic cv-iterator.

        Returns:
            (None, None) if ml_algo is fitted or models are not fitted during training,
            (BestMLAlgo, BestPredictionsLAMLDataset) otherwise.

        """


class DefaultTuner(ParamsTuner):
    """Default realization of ParamsTuner - just take algo's defaults."""

    _name: str = "DefaultTuner"

    def fit(
        self,
        ml_algo: "MLAlgo",
        train_valid_iterator: Optional[TrainValidIterator] = None,
    ) -> Tuple[None, None]:
        """Default fit method - just save defaults.

        Args:
            ml_algo: Algorithm that is tuned.
            train_valid_iterator: Empty.

        Returns:
            Tuple (None, None).
        """
        self._best_params = ml_algo.init_params_on_input(train_valid_iterator=train_valid_iterator)
        return None, None
