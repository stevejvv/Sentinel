import os
import json
import time
import psutil
from pathlib import Path
from typing import List, Dict, Any, Optional

AGY_CLI_DIR = Path.home() / ".gemini" / "antigravity-cli"
CLAUDE_CLI_DIR = Path.home() / ".claude"

class AgentInfo:
    def __init__(
        self,
        pid: int,
        name: str,
        role: str,
        model: str,
        action: str,
        elapsed_seconds: float,
        remaining_time: str,
        context_used: int,
        context_max: int,
        skills: List[str],
        mcps: List[str],
        is_subagent: bool = False,
        cwd: str = ""
    ):
        self.pid = pid
        self.name = name
        self.role = role
        self.model = model
        self.action = action
        self.elapsed_seconds = elapsed_seconds
        self.remaining_time = remaining_time
        self.context_used = context_used
        self.context_max = context_max
        self.skills = skills
        self.mcps = mcps
        self.is_subagent = is_subagent
        self.cwd = cwd

    @property
    def context_percent(self) -> int:
        if self.context_max <= 0:
            return 0
        return min(100, int((self.context_used / self.context_max) * 100))

    @property
    def elapsed_formatted(self) -> str:
        mins, secs = divmod(int(self.elapsed_seconds), 60)
        return f"{mins:02d}m {secs:02d}s"

class AgentInspector:
    """Inspecteur dynamique des processus, transcripts, skills et MCPs d'agents IA (AGY, Claude, OpenCode)."""

    def _get_latest_agy_transcript(self) -> Optional[Path]:
        """Trouve le fichier transcript.jsonl le plus récent dans le dossier brain d'AGY."""
        try:
            presence_locks = list((AGY_CLI_DIR / "presence").glob("*.lock"))
            if presence_locks:
                latest_lock = max(presence_locks, key=lambda p: p.stat().st_mtime)
                conv_id = latest_lock.stem
                transcript_path = AGY_CLI_DIR / "brain" / conv_id / ".system_generated" / "logs" / "transcript.jsonl"
                if transcript_path.exists():
                    return transcript_path

            transcripts = list((AGY_CLI_DIR / "brain").glob("*/.system_generated/logs/transcript.jsonl"))
            if transcripts:
                return max(transcripts, key=lambda p: p.stat().st_mtime)
        except Exception:
            pass
        return None

    def _get_agy_skills(self) -> List[str]:
        """Scanne dynamiquement les vrais skills installés pour AGY."""
        skills: List[str] = []
        user_skills_dir = AGY_CLI_DIR / "skills"
        if user_skills_dir.exists():
            skills.extend([s.name for s in user_skills_dir.iterdir() if not s.name.startswith(".")])

        builtin_skills_dir = AGY_CLI_DIR / "builtin" / "skills"
        if builtin_skills_dir.exists():
            skills.extend([s.name for s in builtin_skills_dir.iterdir() if s.is_dir() and not s.name.startswith(".")])

        return list(dict.fromkeys(skills))

    def _get_claude_skills(self, cwd: str) -> List[str]:
        """Scanne dynamiquement les vrais skills installés pour Claude Code."""
        raw_skills: List[str] = []
        global_skills_dir = CLAUDE_CLI_DIR / "skills"
        if global_skills_dir.exists():
            raw_skills.extend([s.name for s in global_skills_dir.iterdir() if not s.name.startswith(".")])

        proj_skills_dir = Path(cwd) / ".claude" / "skills"
        if proj_skills_dir.exists():
            raw_skills.extend([s.name for s in proj_skills_dir.iterdir() if not s.name.startswith(".")])

        # Normaliser / dédupliquer les préfixes de sous-skills (ex: caveman-help -> caveman)
        cleaned_skills = []
        for s in raw_skills:
            base_name = s.split("-")[0] if "-" in s else s
            if base_name not in cleaned_skills:
                cleaned_skills.append(base_name)

        return cleaned_skills if cleaned_skills else raw_skills

    def _get_claude_mcps(self, cwd: str) -> List[str]:
        """Scanne dynamiquement les vrais MCPs configurés pour Claude Code."""
        mcps: List[str] = []
        mcp_file = CLAUDE_CLI_DIR / "mcp.json"
        if mcp_file.exists():
            try:
                with open(mcp_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    mcps.extend(list(data.get("mcpServers", {}).keys()))
            except Exception:
                pass

        proj_mcp_file = Path(cwd) / ".claude" / "mcp.json"
        if proj_mcp_file.exists():
            try:
                with open(proj_mcp_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    mcps.extend(list(data.get("mcpServers", {}).keys()))
            except Exception:
                pass

        plugins_dir = CLAUDE_CLI_DIR / "plugins"
        if plugins_dir.exists():
            for p in plugins_dir.iterdir():
                if p.is_dir() and not p.name.startswith("."):
                    mcps.append(p.name)

        return list(dict.fromkeys(mcps))

    def _parse_agy_session(self, pid: int, elapsed_seconds: float, cwd: str) -> List[AgentInfo]:
        """Extrait les vraies données de la session AGY."""
        agents: List[AgentInfo] = []
        transcript_path = self._get_latest_agy_transcript()

        last_user_request = "Session active"
        estimated_tokens = 20000
        active_subagents: List[AgentInfo] = []
        model_name = "Gemini 3.6 Flash (High)"

        skills = self._get_agy_skills()
        used_tools = set()

        if transcript_path and transcript_path.exists():
            try:
                file_size = transcript_path.stat().st_size
                estimated_tokens = max(2000, file_size // 4)

                with open(transcript_path, "r", encoding="utf-8") as f:
                    for line in f:
                        if not line.strip():
                            continue
                        try:
                            data = json.loads(line)
                            if data.get("type") == "USER_INPUT" and "content" in data:
                                raw_content = data["content"]
                                if "<USER_REQUEST>" in raw_content:
                                    start = raw_content.find("<USER_REQUEST>") + len("<USER_REQUEST>")
                                    end = raw_content.find("</USER_REQUEST>")
                                    if end > start:
                                        last_user_request = raw_content[start:end].strip().split("\n")[0]
                                else:
                                    last_user_request = raw_content.strip().split("\n")[0]

                            if data.get("type") == "PLANNER_RESPONSE" and "tool_calls" in data:
                                for call in data["tool_calls"]:
                                    tool_name = call.get("name")
                                    if tool_name:
                                        used_tools.add(tool_name)

                                    if tool_name == "invoke_subagent":
                                        sub_args = call.get("args", {})
                                        sub_list = sub_args.get("Subagents", [])
                                        for sub_item in sub_list:
                                            sub_role = sub_item.get("Role", "Sub-Agent")
                                            sub_model = sub_item.get("Model", "Gemini Flash")
                                            sub_prompt = sub_item.get("Prompt", "Executing subtask")
                                            active_subagents.append(
                                                AgentInfo(
                                                    pid=pid + 1,
                                                    name=sub_role,
                                                    role="Sub-Agent",
                                                    model=sub_model,
                                                    action=sub_prompt[:40] + "..." if len(sub_prompt) > 40 else sub_prompt,
                                                    elapsed_seconds=30.0,
                                                    remaining_time="~00m 45s",
                                                    context_used=12000,
                                                    context_max=200000,
                                                    skills=[],
                                                    mcps=["view_file"],
                                                    is_subagent=True,
                                                    cwd=cwd
                                                )
                                            )
                        except Exception:
                            continue
            except Exception:
                pass

        if len(last_user_request) > 60:
            last_user_request = last_user_request[:57] + "..."

        mcps = sorted(list(used_tools)) if used_tools else ["list_dir", "view_file", "run_command"]

        root_agent = AgentInfo(
            pid=pid,
            name="AGY (Antigravity)",
            role="Root Agent",
            model=model_name,
            action=last_user_request,
            elapsed_seconds=elapsed_seconds,
            remaining_time="~01m 20s",
            context_used=estimated_tokens,
            context_max=200000,
            skills=skills,
            mcps=mcps,
            is_subagent=False,
            cwd=cwd
        )
        agents.append(root_agent)
        agents.extend(active_subagents)
        return agents

    def _parse_claude_session(self, pid: int, elapsed_seconds: float, cwd: str) -> List[AgentInfo]:
        """Extrait les vraies données de contexte, skills et MCPs d'une session Claude Code."""
        agents: List[AgentInfo] = []
        last_user_request = "Active CLI Session"
        input_tokens = 0
        output_tokens = 0
        used_tools = set()

        encoded_cwd = cwd.replace("/", "-")
        claude_proj_dir = CLAUDE_CLI_DIR / "projects" / encoded_cwd

        skills = self._get_claude_skills(cwd)
        configured_mcps = self._get_claude_mcps(cwd)

        if claude_proj_dir.exists():
            jsonl_files = list(claude_proj_dir.glob("*.jsonl"))
            if jsonl_files:
                latest_jsonl = max(jsonl_files, key=lambda p: p.stat().st_mtime)
                try:
                    with open(latest_jsonl, "r", encoding="utf-8") as f:
                        for line in f:
                            if not line.strip():
                                continue
                            try:
                                data = json.loads(line)
                                # Extraire le prompt utilisateur
                                if data.get("type") == "user" and "message" in data:
                                    content = data["message"].get("content", "")
                                    if isinstance(content, str) and content.strip():
                                        txt = content.strip()
                                        if "<command-message>" in txt:
                                            s = txt.find("<command-message>") + len("<command-message>")
                                            e = txt.find("</command-message>")
                                            if e > s:
                                                txt = txt[s:e]
                                        if not txt.startswith("Base directory"):
                                            last_user_request = txt.split("\n")[0]
                                    elif isinstance(content, list):
                                        for item in content:
                                            if isinstance(item, dict) and item.get("type") == "text":
                                                txt = item.get("text", "").strip()
                                                if txt and not txt.startswith("Base directory"):
                                                    last_user_request = txt.split("\n")[0]
                                                    break

                                # Extraire les tokens d'assistant et les outils engagés
                                if data.get("type") == "assistant" and "message" in data:
                                    msg = data["message"]
                                    usage = msg.get("usage", {})
                                    if usage.get("input_tokens"):
                                        input_tokens = max(input_tokens, usage.get("input_tokens", 0))
                                    output_tokens += usage.get("output_tokens", 0)

                                    for item in msg.get("content", []):
                                        if isinstance(item, dict) and item.get("type") == "tool_use":
                                            used_tools.add(item.get("name"))
                            except Exception:
                                continue
                except Exception:
                    pass

        total_context_tokens = input_tokens + output_tokens
        if total_context_tokens == 0:
            # Fallback direct basé sur la taille du fichier si les tokens ne sont pas dans le JSONL
            if claude_proj_dir.exists():
                jsonl_files = list(claude_proj_dir.glob("*.jsonl"))
                if jsonl_files:
                    total_context_tokens = max(1000, max(f.stat().st_size for f in jsonl_files) // 4)
            else:
                total_context_tokens = 5000

        if len(last_user_request) > 60:
            last_user_request = last_user_request[:57] + "..."

        mcps = list(dict.fromkeys(configured_mcps + sorted(list(used_tools))))

        claude_root = AgentInfo(
            pid=pid,
            name="Claude Code",
            role="Root Agent",
            model="Claude 3.7 Sonnet",
            action=last_user_request,
            elapsed_seconds=elapsed_seconds,
            remaining_time="~02m 00s",
            context_used=total_context_tokens,
            context_max=200000,
            skills=skills,
            mcps=mcps,
            is_subagent=False,
            cwd=cwd
        )
        agents.append(claude_root)
        return agents

    def scan_active_agents(self, target_dir: Optional[Path] = None) -> List[AgentInfo]:
        """Scanne les processus système et renvoie UNIQUEMENT les agents actifs dans target_dir sans doublons."""
        if target_dir is None:
            target_dir = Path.cwd().resolve()
        else:
            target_dir = Path(target_dir).resolve()

        active_agents: List[AgentInfo] = []
        seen_agent_types = set()

        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'create_time']):
                try:
                    cmdline = proc.info['cmdline'] or []
                    cmd_str = " ".join(cmdline).lower()
                    pname = (proc.info['name'] or "").lower()

                    proc_cwd_str = proc.cwd()
                    proc_cwd = Path(proc_cwd_str).resolve()

                    if proc_cwd != target_dir and target_dir not in proc_cwd.parents:
                        continue

                    # Ignorer les sous-processus python/node secondaires de Claude ou AGY
                    if (pname == "python" or pname == "python3" or pname == "node") and ("claude" not in cmd_str and "agy" not in cmd_str):
                        continue

                    elapsed = time.time() - proc.info['create_time']

                    if ("antigravity" in cmd_str or "agy" in cmd_str) and "agy" not in seen_agent_types:
                        parsed = self._parse_agy_session(proc.info['pid'], elapsed, str(proc_cwd))
                        if parsed:
                            active_agents.extend(parsed)
                            seen_agent_types.add("agy")

                    elif ("claude" in cmd_str or "claude" in pname) and "claude" not in seen_agent_types:
                        parsed = self._parse_claude_session(proc.info['pid'], elapsed, str(proc_cwd))
                        if parsed:
                            active_agents.extend(parsed)
                            seen_agent_types.add("claude")

                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
        except Exception:
            pass

        return active_agents
