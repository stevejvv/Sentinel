import httpx
from typing import Optional
from sentinel.adapters.base import BaseLLMAdapter

class OllamaHTTPAdapter(BaseLLMAdapter):
    """Adaptateur HTTP pour le serveur Ollama local."""
    
    def __init__(self, url: str = "http://127.0.0.1:11434", model: str = "qwen2.5-coder:32b"):
        self.url = url.rstrip("/")
        self.model = model

    async def ping(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                res = await client.get(f"{self.url}/api/tags")
                return res.status_code == 200
        except Exception:
            return False

    async def generate(self, prompt: str, system_prompt: str = "") -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "system": system_prompt,
            "stream": False
        }
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                res = await client.post(f"{self.url}/api/generate", json=payload)
                if res.status_code == 200:
                    return res.json().get("response", "")
                return f"[Erreur Ollama HTTP {res.status_code}]"
        except Exception as e:
            return f"[Erreur de connexion Ollama: {str(e)}]"
