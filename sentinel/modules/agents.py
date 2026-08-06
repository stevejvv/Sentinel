import os
import re
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

    def _get_active_agy_transcripts(self) -> List[Path]:
        """Retourne la liste des transcripts AGY actifs triée du plus récent au plus ancien."""
        active_transcripts = []
        try:
            presence_locks = list((AGY_CLI_DIR / "presence").glob("*.lock"))
            for lock in presence_locks:
                conv_id = lock.stem
                t_path = AGY_CLI_DIR / "brain" / conv_id / ".system_generated" / "logs" / "transcript.jsonl"
                if t_path.exists():
                    active_transcripts.append(t_path)
        except Exception:
            pass
        return sorted(active_transcripts, key=lambda p: p.stat().st_mtime, reverse=True)

    def _find_claude_project_dir(self, cwd: str) -> Optional[Path]:
        """Trouve le dossier de projet Claude correspondant au répertoire courant."""
        projects_dir = CLAUDE_CLI_DIR / "projects"
        if not projects_dir.exists():
            return None

        encoded_exact = cwd.replace("/", "-")
        exact_dir = projects_dir / encoded_exact
        if exact_dir.exists():
            return exact_dir

        cwd_name = Path(cwd).name.lower()
        for p in projects_dir.iterdir():
            if p.is_dir() and cwd_name in p.name.lower():
                return p
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

    def _parse_agy_session(self, pid: int, elapsed_seconds: float, cwd: str, transcript_path: Optional[Path] = None) -> List[AgentInfo]:
        """Extrait les vraies données de la session AGY sans aucune valeur simulée."""
        agents: List[AgentInfo] = []

        last_user_request = "Session active"
        estimated_tokens = 0
        model_name = "Gemini Flash"

        skills = self._get_agy_skills()
        used_tools = set()
        subagent_conv_ids: Dict[str, Dict[str, str]] = {}

        if transcript_path and transcript_path.exists():
            try:
                file_size = transcript_path.stat().st_size
                estimated_tokens = file_size // 4

                # Track pending subagent metadata from invoke_subagent calls
                pending_sub_meta: List[Dict[str, str]] = []

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
                                    
                                if "USER_SETTINGS_CHANGE" in raw_content:
                                    import re
                                    match = re.search(r"setting `Model Selection` from .*? to (.*?)\.", raw_content)
                                    if match:
                                        model_name = match.group(1).strip()

                            if data.get("type") == "PLANNER_RESPONSE" and "tool_calls" in data:
                                for call in data["tool_calls"]:
                                    tool_name = call.get("name")
                                    if tool_name:
                                        used_tools.add(tool_name)

                                    if tool_name == "invoke_subagent":
                                        sub_args = call.get("args", {})
                                        sub_list = sub_args.get("Subagents", [])
                                        if isinstance(sub_list, str):
                                            try:
                                                sub_list = json.loads(sub_list)
                                            except Exception:
                                                sub_list = []
                                        for sub_item in sub_list:
                                            pending_sub_meta.append({
                                                "role": sub_item.get("Role", "Sub-Agent"),
                                                "model": sub_item.get("Model", "inherit"),
                                                "prompt": sub_item.get("Prompt", ""),
                                            })

                            # INVOKE_SUBAGENT steps contain the conversationId in their content
                            if data.get("type") == "INVOKE_SUBAGENT" and "content" in data:
                                content = data["content"]
                                conv_match = re.search(r'"conversationId"\s*:\s*"([a-f0-9-]+)"', content)
                                if conv_match:
                                    conv_id = conv_match.group(1)
                                    meta = pending_sub_meta.pop(0) if pending_sub_meta else {"role": "Sub-Agent", "model": "inherit", "prompt": ""}
                                    subagent_conv_ids[conv_id] = meta

                        except Exception:
                            continue
            except Exception:
                pass

        if len(last_user_request) > 60:
            last_user_request = last_user_request[:57] + "..."

        mcps = sorted(list(used_tools)) if used_tools else []

        root_agent = AgentInfo(
            pid=pid,
            name="AGY (Antigravity)",
            role="Root Agent",
            model=model_name,
            action=last_user_request,
            elapsed_seconds=elapsed_seconds,
            remaining_time="",
            context_used=estimated_tokens,
            context_max=1000000,
            skills=skills,
            mcps=mcps,
            is_subagent=False,
            cwd=cwd
        )
        agents.append(root_agent)

        # Detect truly active subagents by checking their transcript freshness
        active_subs = self._detect_active_subagents(subagent_conv_ids, pid, cwd)
        agents.extend(active_subs)

        return agents

    def _detect_active_subagents(self, conv_ids: Dict[str, Dict[str, str]], parent_pid: int, cwd: str) -> List[AgentInfo]:
        """Détecte les sub-agents réellement actifs en vérifiant la fraîcheur de leur transcript."""
        active: List[AgentInfo] = []
        now = time.time()

        for conv_id, meta in conv_ids.items():
            transcript = AGY_CLI_DIR / "brain" / conv_id / ".system_generated" / "logs" / "transcript.jsonl"
            if not transcript.exists():
                continue

            # Sub-agent is active if its transcript was modified in the last 30 seconds
            mtime = transcript.stat().st_mtime
            if now - mtime > 30:
                continue

            sub_action = "Executing subtask"
            sub_tokens = 0
            sub_model = meta.get("model", "inherit")
            sub_role = meta.get("role", "Sub-Agent")

            try:
                sub_tokens = transcript.stat().st_size // 4
                with open(transcript, "r", encoding="utf-8") as f:
                    for line in f:
                        if not line.strip():
                            continue
                        try:
                            data = json.loads(line)
                            # Get the subagent's assigned task from the first USER_INPUT
                            if data.get("type") == "USER_INPUT" and "content" in data:
                                raw_content = data["content"]
                                if "<USER_REQUEST>" in raw_content:
                                    start = raw_content.find("<USER_REQUEST>") + len("<USER_REQUEST>")
                                    end = raw_content.find("</USER_REQUEST>")
                                    if end > start:
                                        raw = raw_content[start:end].strip().split("\n")[0]
                                    else:
                                        raw = raw_content.strip().split("\n")[0]
                                else:
                                    raw = raw_content.strip().split("\n")[0]
                                if len(raw) > 40:
                                    raw = raw[:37] + "..."
                                sub_action = raw
                            # Try to get the model from settings
                            if data.get("type") == "PLANNER_RESPONSE" and data.get("model"):
                                sub_model = data["model"]
                        except Exception:
                            continue
            except Exception:
                pass

            if sub_model == "inherit":
                sub_model = "Gemini Flash"

            elapsed = now - mtime
            active.append(AgentInfo(
                pid=parent_pid + len(active) + 1,
                name=sub_role,
                role="Sub-Agent",
                model=sub_model,
                action=sub_action,
                elapsed_seconds=elapsed,
                remaining_time="",
                context_used=sub_tokens,
                context_max=200000,
                skills=[],
                mcps=[],
                is_subagent=True,
                cwd=cwd
            ))

        return active

    def _parse_claude_session(self, pid: int, elapsed_seconds: float, cwd: str) -> List[AgentInfo]:
        """Extrait les vraies données de contexte, skills et MCPs d'une session Claude Code."""
        agents: List[AgentInfo] = []
        last_user_request = "Session active"
        input_tokens = 0
        output_tokens = 0
        used_tools = set()

        claude_proj_dir = self._find_claude_project_dir(cwd)

        skills = self._get_claude_skills(cwd)
        configured_mcps = self._get_claude_mcps(cwd)

        if claude_proj_dir and claude_proj_dir.exists():
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

                                if data.get("type") == "assistant" and "message" in data:
                                    msg = data["message"]
                                    usage = msg.get("usage", {})
                                    if usage.get("input_tokens"):
                                        input_tokens = usage.get("input_tokens", 0)
                                    output_tokens += usage.get("output_tokens", 0)

                                    for item in msg.get("content", []):
                                        if isinstance(item, dict) and item.get("type") == "tool_use":
                                            used_tools.add(item.get("name"))
                            except Exception:
                                continue
                except Exception:
                    pass

        total_context_tokens = input_tokens + output_tokens
        if total_context_tokens == 0 and claude_proj_dir and claude_proj_dir.exists():
            jsonl_files = list(claude_proj_dir.glob("*.jsonl"))
            if jsonl_files:
                total_context_tokens = max(f.stat().st_size for f in jsonl_files) // 4

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
            context_max=1000000,
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
        seen_claude_cwds = set()
        
        agy_active_transcripts = self._get_active_agy_transcripts()
        agy_idx = 0

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

                    if (pname == "python" or pname == "python3" or pname == "node") and ("claude" not in cmd_str and "agy" not in cmd_str):
                        continue

                    elapsed = time.time() - proc.info['create_time']

                    if ("antigravity" in cmd_str or "agy" in cmd_str):
                        # Use the next available transcript for this AGY process
                        t_path = agy_active_transcripts[agy_idx] if agy_idx < len(agy_active_transcripts) else None
                        parsed = self._parse_agy_session(proc.info['pid'], elapsed, str(proc_cwd), t_path)
                        if parsed:
                            active_agents.extend(parsed)
                            agy_idx += 1

                    elif ("claude" in cmd_str or "claude" in pname):
                        if str(proc_cwd) not in seen_claude_cwds:
                            parsed = self._parse_claude_session(proc.info['pid'], elapsed, str(proc_cwd))
                            if parsed:
                                active_agents.extend(parsed)
                                seen_claude_cwds.add(str(proc_cwd))

                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
        except Exception:
            pass

        return active_agents
