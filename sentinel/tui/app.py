from typing import List
from pathlib import Path
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Label, Input
from textual.containers import Vertical, Grid, Horizontal, VerticalScroll
from textual.theme import Theme
from sentinel.modules.agents import AgentInspector, AgentInfo

# 1. Thème Claude Code Dark (Amber Chaud & Anthracite Pro)
CLAUDE_DARK_THEME = Theme(
    name="claude-dark",
    primary="#D97706",       # Amber Chaud Anthropic
    secondary="#38BDF8",     # Cyan Doux
    warning="#F59E0B",
    error="#EF4444",
    success="#10B981",
    accent="#F97316",        # Orange
    foreground="#ECECF1",    # Blanc Cassé Pro
    background="#171717",    # Anthracite Sombre
    surface="#262626",       # Surface Sombre
    panel="#404040",         # Séparateurs
    dark=True,
)

# 2. Thème Herdr Dark (Cyan Électrique & Ardoise Midnight)
HERDR_DARK_THEME = Theme(
    name="herdr-dark",
    primary="#00F0FF",       # Cyan Électrique Herdr
    secondary="#818CF8",     # Indigo
    warning="#FBBF24",
    error="#F87171",
    success="#34D399",
    accent="#00F0FF",
    foreground="#F8FAFC",    # Blanc Cassé Slate
    background="#0B0F17",    # Midnight Slate
    surface="#151D2A",       # Surface Slate
    panel="#1E293B",
    dark=True,
)

# 3. Thème OpenCode / VS Code Dark Plus
OPENCODE_DARK_THEME = Theme(
    name="opencode-dark",
    primary="#61AFEF",       # OpenCode / VS Code Blue
    secondary="#C678DD",     # Violet Muted
    warning="#E5C07B",
    error="#E06C75",
    success="#98C379",
    accent="#56B6C2",
    foreground="#ABB2BF",    # Code Gray
    background="#1E1E1E",    # VS Code Dark background
    surface="#252526",       # Side Bar Gray
    panel="#333333",
    dark=True,
)

# 4. Thème Matrix Terminal (Vert Émeraude Monochrome Geek)
MATRIX_GEEK_THEME = Theme(
    name="matrix-geek",
    primary="#00FF66",       # Vert Matrix Émeraude
    secondary="#00DD55",
    warning="#FFB000",
    error="#FF453A",
    success="#00FF66",
    accent="#00FF66",
    foreground="#E0F8E0",    # Blanc Teinté Vert
    background="#080C08",    # Terminal Noir Épuré
    surface="#101810",
    panel="#1B281B",
    dark=True,
)

# 5. Thème Monokai Pro (Charcoal & Pastels Pro)
MONOKAI_PRO_THEME = Theme(
    name="monokai-pro",
    primary="#FFD866",       # Monokai Gold
    secondary="#78DCE8",     # Cyan
    warning="#FC9867",       # Orange
    error="#FF6188",         # Red
    success="#A9DC76",       # Green
    accent="#AB9DF2",        # Purple
    foreground="#FCFCFA",    # Off-White
    background="#2D2A2E",    # Monokai Charcoal
    surface="#3A383C",
    panel="#4A474D",
    dark=True,
)

class TopStatusBanner(Static):
    """Bannière minimale sans bordures ni émojis."""
    def compose(self) -> ComposeResult:
        proj_name = Path.cwd().name
        yield Label(f"[bold primary]SENTINEL[/bold primary] [dim]v0.1.0[/dim]  │  [dim]Project:[/dim] [bold white]{proj_name}[/bold white]  │  [dim]Watchdog:[/dim] [bold success]Local x99 (Qwen 32B)[/bold success]", id="banner-text")

class RootAgentPane(Static):
    """Orchestration directe et minimale des agents & sub-agents filtrée par projet."""
    def compose(self) -> ComposeResult:
        yield Label("❯ AGENT ORCHESTRATION", classes="pane-title")
        yield Vertical(id="agent-tree-content")

    def update_agents(self, agents: List[AgentInfo]) -> None:
        """Mise à jour dynamique de l'arborescence des agents."""
        container = self.query_one("#agent-tree-content", Vertical)
        container.remove_children()

        if not agents:
            curr_dir = Path.cwd().name
            container.mount(Label(f"[dim][OFFLINE] Aucune session d'agent IA active dans ce projet ({curr_dir})[/dim]"))
            return

        root_agents = [a for a in agents if not a.is_subagent]
        sub_agents = [a for a in agents if a.is_subagent]

        for root in root_agents:
            warn = "[yellow][WARN][/yellow] [cyan]/compact[/cyan] recommended" if root.context_percent >= 60 else ""
            container.mount(Label(f"[bold success][RUNNING][/bold success] [bold white]{root.name}[/bold white] [dim]({root.model})[/dim]"))
            container.mount(Label(f" ├─ Action: [bold primary]{root.action}[/bold primary]"))
            container.mount(Label(f" ├─ Context: [bold primary]{root.context_percent}%[/bold primary] [dim]({root.context_used // 1000}k / {root.context_max // 1000}k)[/dim]  {warn}"))
            skills_str = ", ".join(root.skills) if root.skills else "aucun"
            mcps_str = ", ".join(root.mcps) if root.mcps else "aucun"
            container.mount(Label(f" ├─ Active Skills: [dim]{skills_str}[/dim]"))
            container.mount(Label(f" └─ Active MCPs: [dim]{mcps_str}[/dim]\n"))

        if sub_agents:
            container.mount(Label(" └─ > SUB-AGENTS"))
            for sub in sub_agents:
                container.mount(Label(f"    [bold success][RUNNING][/bold success] [bold white]{sub.name}[/bold white] [dim]({sub.model})[/dim]"))
                container.mount(Label(f"    ├─ Action: [dim]{sub.action}[/dim]"))
                container.mount(Label(f"    └─ Tokens: [bold primary]{sub.context_used // 1000}k[/bold primary] [dim]({sub.context_percent}%)[/dim]"))

class GitStatusPane(Static):
    """Statut Git épuré."""
    def compose(self) -> ComposeResult:
        yield Label("❯ VERSION CONTROL (Git)", classes="pane-title")
        yield Label("Branch: [bold primary]main[/bold primary]  │  [yellow]3 Modified[/yellow]")
        yield Label("Diff: [bold success]+142[/bold success] [bold error]-38[/bold error] lines\n")
        yield Label("src/engine/board.py       [success]+98[/success] [error]-12[/error]")
        yield Label("tests/test_forcing.py     [success]+44[/success] [error]-26[/error]")
        yield Label("include/bitboard.hpp      [dim]+0 -0[/dim]")

class SecurityAuditPane(Static):
    """Audit de sécurité épuré."""
    def compose(self) -> ComposeResult:
        yield Label("❯ SECURITY & AUDIT", classes="pane-title")
        yield Label("[success][OK][/success] src/engine/board.py [dim]Clean[/dim]")
        yield Label("[yellow][WARN][/yellow] src/engine/eval.py [dim]L112: Index check[/dim]")
        yield Label("[success][OK][/success] Secrets Scanner: [dim]No API keys leaked[/dim]")

class TestPerfPane(Static):
    """Métriques de tests et perf épurées."""
    def compose(self) -> ComposeResult:
        yield Label("❯ TESTS & PERFORMANCE", classes="pane-title")
        yield Label("Build: [bold success][PASS] GCC 14 -O3[/bold success]")
        yield Label("Tests: [bold success][PASS] 142/142 Passed[/bold success]")
        yield Label("Speed: [bold primary]14.8M NPS[/bold primary] [success](+4.2%)[/success]")
        yield Label("Memory: [dim]1.2 GB / 64 GB[/dim]")

class TimelinePane(Static):
    """Chronologie épurée."""
    def compose(self) -> ComposeResult:
        yield Label("❯ TIMELINE", classes="pane-title")
        yield Label("[dim]23:15[/dim] Session initialized")
        yield Label("[dim]23:20[/dim] Commit 'Add L4 tree'")
        yield Label("[dim]23:28[/dim] Sub-agent agy started")
        yield Label("[dim]23:35[/dim] Performance alert resolved")

class AgentPromptBar(Horizontal):
    """Barre d'invite de commande type Claude Code / AGY sans encadrés."""
    def compose(self) -> ComposeResult:
        yield Label("❯ ", id="prompt-symbol")
        yield Input(placeholder="Ask a question, run a command (/compact, /clear)...", id="chat-input")

class SentinelApp(App):
    """Application TUI Minimaliste & Directe (Filtrage de projet strict)."""

    TITLE = "Sentinel CLI"
    SUB_TITLE = "Terminal AI Watchdog"

    THEMES_MAP = {
        "claude-dark": CLAUDE_DARK_THEME,
        "herdr-dark": HERDR_DARK_THEME,
        "opencode-dark": OPENCODE_DARK_THEME,
        "matrix-geek": MATRIX_GEEK_THEME,
        "monokai-pro": MONOKAI_PRO_THEME,
    }
    THEMES_CYCLE = list(THEMES_MAP.keys())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for theme_obj in self.THEMES_MAP.values():
            self.register_theme(theme_obj)
        self.theme = "claude-dark"
        self.current_theme_index = 0
        self.inspector = AgentInspector()

    CSS = """
    Screen {
        layout: vertical;
        padding: 0;
        background: $background;
    }

    TopStatusBanner {
        background: $surface;
        color: $primary;
        border: none;
        border-bottom: solid $panel;
        height: 3;
        content-align: center middle;
        padding: 0 2;
    }

    #grid-container {
        height: 1fr;
        overflow-y: auto;
    }

    #main-grid {
        layout: grid;
        grid-size: 2 2;
        grid-gutter: 1 2;
        padding: 1 2;
    }

    RootAgentPane {
        height: auto;
        padding: 0 2;
        border-left: solid $panel;
        margin: 1 2 0 2;
    }

    Static {
        background: $background;
        border: none;
        border-left: solid $panel;
        padding: 0 1;
    }

    Static:focus {
        border-left: solid $primary;
    }

    .pane-title {
        color: $primary;
        text-style: bold;
        border: none;
        border-bottom: solid $panel;
        margin-bottom: 1;
        padding-bottom: 0;
    }

    AgentPromptBar {
        height: 3;
        padding: 0 2;
        background: $surface;
        border-top: solid $panel;
        align: left middle;
    }

    #prompt-symbol {
        color: $primary;
        text-style: bold;
        width: 3;
        padding: 0;
        border: none;
        background: transparent;
    }

    #chat-input {
        width: 1fr;
        border: none;
        background: transparent;
        color: $foreground;
        padding: 0;
    }

    #chat-input:focus {
        border: none;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("ctrl+c", "quit", "Quit"),
        ("t", "cycle_theme", "Change Theme"),
        ("r", "refresh", "Refresh"),
        ("s", "summary", "Export Summary"),
        ("c", "focus_chat", "Prompt Agent"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield TopStatusBanner()
        
        with VerticalScroll(id="grid-container"):
            yield RootAgentPane()
            with Grid(id="main-grid"):
                yield GitStatusPane()
                yield SecurityAuditPane()
                yield TestPerfPane()
                yield TimelinePane()

        yield AgentPromptBar()
        yield Footer()

    def on_mount(self) -> None:
        """Initialise la détection en direct des agents du projet courant."""
        self.refresh_agents()
        self.set_interval(2.0, self.refresh_agents)

    def refresh_agents(self) -> None:
        """Met à jour les données réelles des agents scannés dans le répertoire courant."""
        try:
            agents = self.inspector.scan_active_agents()
            root_pane = self.query_one(RootAgentPane)
            root_pane.update_agents(agents)
        except Exception:
            pass

    def on_resize(self, event) -> None:
        try:
            grid = self.query_one("#main-grid", Grid)
            if event.size.width < 100:
                grid.styles.grid_size_columns = 1
            else:
                grid.styles.grid_size_columns = 2
        except Exception:
            pass

    def action_cycle_theme(self) -> None:
        self.current_theme_index = (self.current_theme_index + 1) % len(self.THEMES_CYCLE)
        new_theme = self.THEMES_CYCLE[self.current_theme_index]
        self.theme = new_theme
        self.notify(f"Active Theme: [bold primary]{new_theme}[/bold primary]", title="Theme Switcher")

    def action_focus_chat(self) -> None:
        chat_input = self.query_one("#chat-input", Input)
        chat_input.focus()

if __name__ == "__main__":
    app = SentinelApp()
    app.run()
