from abc import ABC, abstractmethod

class BaseSkill(ABC):
    @property
    @abstractmethod
    def name(self) -> str: pass

    @property
    @abstractmethod
    def description(self) -> str: pass

    @property
    @abstractmethod
    def trigger_phrases(self) -> list: pass

    @abstractmethod
    async def run(self, brain, params: dict = None) -> dict:
        """
        Executes the skill's multi-step sequence.
        Returns: {"status", "message", "receipt"}
        """
        pass
