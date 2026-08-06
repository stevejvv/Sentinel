from abc import ABC, abstractmethod

class BaseLLMAdapter(ABC):
    """Classe de base abstraite pour tous les adaptateurs LLM Sentinel."""
    
    @abstractmethod
    async def ping(self) -> bool:
        """Vérifie la disponibilité et la latence de l'adaptateur."""
        pass

    @abstractmethod
    async def generate(self, prompt: str, system_prompt: str = "") -> str:
        """Génère une réponse textuelle depuis le modèle LLM."""
        pass
