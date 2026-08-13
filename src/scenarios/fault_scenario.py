from abc import ABC, abstractmethod
from typing import Any


class FaultScenario(ABC):
    """
    Abstract class for managing scenarios of the code.
    """

    @abstractmethod
    def run(self, buggy: bool) -> Any:
        """
        Run scenario.
        :param buggy: If True, execute the buggy scenario. Otherwise, execute the positive scenario.
        :return: Result of the scenario
        """
        pass
