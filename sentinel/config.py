import json
from pathlib import Path
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

GLOBAL_CONFIG_DIR = Path.home() / ".config" / "sentinel"
GLOBAL_CONFIG_PATH = GLOBAL_CONFIG_DIR / "config.json"
LOCAL_CONFIG_PATH = Path(".sentinel.json")

class LLMAdapterConfig(BaseModel):
    type: str  # "ollama_http" or "subprocess"
    url: Optional[str] = None
    model: Optional[str] = None
    command: Optional[str] = None

class SentinelConfig(BaseModel):
    version: str = "0.1.0"
    default_adapter: str = "local_x99"
    test_command: str = "pytest"
    security_scanner_enabled: bool = True
    llm_adapters: Dict[str, LLMAdapterConfig] = Field(default_factory=lambda: {
        "local_x99": LLMAdapterConfig(
            type="ollama_http",
            url="http://127.0.0.1:11434",
            model="qwen2.5-coder:32b"
        ),
        "gemini_cli": LLMAdapterConfig(
            type="subprocess",
            command="agy -p --model 'Gemini 3.6 Flash (High)'"
        ),
        "claude_cli": LLMAdapterConfig(
            type="subprocess",
            command="claude -p"
        )
    })

def load_config() -> SentinelConfig:
    """Charge et fusionne les configurations globale et locale."""
    config_data: Dict[str, Any] = {}
    
    # 1. Charger la config globale si elle existe
    if GLOBAL_CONFIG_PATH.exists():
        try:
            with open(GLOBAL_CONFIG_PATH, "r", encoding="utf-8") as f:
                config_data.update(json.load(f))
        except Exception:
            pass

    # 2. Surcharger avec la config locale du projet si présente
    if LOCAL_CONFIG_PATH.exists():
        try:
            with open(LOCAL_CONFIG_PATH, "r", encoding="utf-8") as f:
                local_data = json.load(f)
                config_data.update(local_data)
        except Exception:
            pass

    if not config_data:
        return SentinelConfig()
    
    return SentinelConfig(**config_data)

def save_global_config(config: SentinelConfig) -> None:
    """Sauvegarde la configuration globale dans ~/.config/sentinel/config.json."""
    GLOBAL_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(GLOBAL_CONFIG_PATH, "w", encoding="utf-8") as f:
        f.write(config.model_dump_json(indent=2))

def save_local_config(config_dict: Dict[str, Any]) -> None:
    """Sauvegarde la configuration spécifique au projet dans .sentinel.json."""
    with open(LOCAL_CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config_dict, f, indent=2)
