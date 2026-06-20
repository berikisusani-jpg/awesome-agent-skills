from abc import ABC, abstractmethod

class BaseIntegration(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def available(self) -> bool:
        """Returns True if the integration is correctly configured and reachable."""
        pass

    @abstractmethod
    async def execute(self, action: str, params: dict = None) -> dict:
        """
        Executes the specified action with params.
        Returns a structured response:
        {
            "status": "success" | "error" | "not_implemented" | "demo_mode",
            "message": "...",
            "receipt": {"type": "...", "data": "...", "timestamp": "..."}
        }
        """
        pass
