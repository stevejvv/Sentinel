import asyncio
import shutil
from sentinel.adapters.base import BaseLLMAdapter

class SubprocessCLIAdapter(BaseLLMAdapter):
    """Adaptateur Subprocess pour les CLI d'agents (claude, agy, opencode)."""
    
    def __init__(self, command: str):
        self.command = command
        self.binary = command.split()[0] if command else ""

    async def ping(self) -> bool:
        return shutil.which(self.binary) is not None

    async def generate(self, prompt: str, system_prompt: str = "") -> str:
        full_command = f"{self.command} '{prompt}'"
        try:
            proc = await asyncio.create_subprocess_shell(
                full_command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await proc.communicate()
            if proc.returncode == 0:
                return stdout.decode("utf-8").strip()
            return f"[Erreur Subprocess {proc.returncode}: {stderr.decode('utf-8')}]"
        except Exception as e:
            return f"[Erreur d'exécution Subprocess: {str(e)}]"
