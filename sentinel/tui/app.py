from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Label, ProgressBar, Input
from textual.containers import Vertical, Grid, Horizontal, VerticalScroll
from textual.theme import Theme

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
    """Bannière minimale sans bordures type CLI agent."""
    def compose(self) -> ComposeResult:
        yield Label("🛡️ [bold primary]SENTINEL[/bold primary] [dim]v0.1.0[/dim]  │  [dim]Project:[/dim] [bold white]SENTINEL[/bold white]  │  [dim]Watchdog:[/dim] [bold success]Local x99 (Qwen 32B)[/bold success]", id="banner-text")

class AgentCard(Static):
    """Ligne d'agent minimaliste sans encadré."""
    def __init__(self, agent_name: str, role: str, action: str, elapsed: str, status: str = "running", **kwargs):
        super().__init__(**kwargs)
        self.agent_name = agent_name
        self.role = role
        self.action = action
        self.elapsed = elapsed
        self.status = status

    def compose(self) -> ComposeResult:
        status_icon = "🟢" if self.status == "running" else "🟡"
        yield Label(f"{status_icon} [bold white]{self.agent_name}[/bold white] [dim]({self.role})[/dim]")
        yield Label(f"   [dim]└─[/dim] Action: [bold primary]{self.action}[/bold primary]")
        yield Label(f"   [dim]└─ Elapsed:[/dim] [bold success]{self.elapsed}[/bold success]  │  [dim]MCPs:[/dim] [yellow]sqlite, github[/yellow]")

class TokenGauges(Static):
    """Panneau de contexte minimaliste sans encadré."""
    def compose(self) -> ComposeResult:
        yield Label("❯ FENÊTRE DE CONTEXTE & TOKENS", classes="pane-title")
        yield Label("📊 Contexte: [bold primary]68%[/bold primary] [dim](136k / 200k tokens)[/dim]")
        pb = ProgressBar(total=100, show_eta=False, id="context-bar")
        pb.progress = 68
        yield pb
        yield Label("💰 Session: [bold success]$0.42[/bold success] [dim](48k in, 4k out)[/dim]")
        yield Label("⚠️ [yellow]Rec:[/yellow] Exécuter [bold primary]/compact[/bold primary]")

class GitStatusPane(Static):
    """Statut Git épuré."""
    def compose(self) -> ComposeResult:
        yield Label("❯ VERSION CONTROL (Git)", classes="pane-title")
        yield Label("Branch: [bold primary]main[/bold primary]  │  [yellow]3 Modified[/yellow]")
        yield Label("Diff: [bold success]+142[/bold success] [bold error]-38[/bold error] lines")
        yield Label("📄 [white]src/engine/board.py[/white]      [success]+98[/success] [error]-12[/error]")
        yield Label("📄 [white]tests/test_forcing.py[/white]    [success]+44[/success] [error]-26[/error]")

class SecurityAuditPane(Static):
    """Audit de sécurité épuré."""
    def compose(self) -> ComposeResult:
        yield Label("❯ SÉCURITÉ & SENTINELLE", classes="pane-title")
        yield Label("🟢 [white]src/engine/board.py[/white] [dim]Clean[/dim]")
        yield Label("⚠️ [yellow]src/engine/eval.py[/yellow] [dim]L112: Index check[/dim]")
        yield Label("🔒 [success]Secrets:[/success] [dim]No API keys leaked[/dim]")

class TestPerfPane(Static):
    """Métriques de tests et perf épurées."""
    def compose(self) -> ComposeResult:
        yield Label("❯ TESTS & PERFORMANCES", classes="pane-title")
        yield Label("🔨 Build: [bold success]PASS (GCC 14 -O3)[/bold success]")
        yield Label("🧪 Tests: [bold success]142/142 Passed[/bold success]")
        yield Label("⚡ Speed: [bold primary]14.8M NPS[/bold primary] [success](+4.2%)[/success]")

class TimelinePane(Static):
    """Chronologie épurée."""
    def compose(self) -> ComposeResult:
        yield Label("❯ CHRONOLOGIE", classes="pane-title")
        yield Label("🕒 [dim]23:15[/dim] Session init")
        yield Label("🕒 [dim]23:20[/dim] Commit 'Add L4 tree'")
        yield Label("🕒 [dim]23:35[/dim] Perf alert resolved")

class AgentPromptBar(Horizontal):
    """Barre d'invite de commande type Claude Code / AGY sans encadrés."""
    def compose(self) -> ComposeResult:
        yield Label("❯ ", id="prompt-symbol")
        yield Input(placeholder="Ask a question, run a command (/compact, /clear)...", id="chat-input")

class SentinelApp(App):
    """Application TUI Pro & Geek (Style Claude Code, Herdr & OpenCode)."""

    TITLE = "Sentinel CLI"
    SUB_TITLE = "Terminal AI Watchdog"

    # 5 Thèmes Pro & Geek inspirés des agents et éditeurs de code
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
        # Enregistrer tous les thèmes pro
        for theme_obj in self.THEMES_MAP.values():
            self.register_theme(theme_obj)
        self.theme = "claude-dark"
        self.current_theme_index = 0

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
        grid-size: 2 3;
        grid-gutter: 1 2;
        padding: 1 2;
    }

    /* Panneaux sans encadrés : fond transparent/subtil avec bordure gauche d'accentuation */
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

    ProgressBar {
        margin-top: 1;
        margin-bottom: 1;
        height: 1;
        border: none;
    }

    ProgressBar > .bar--bar {
        color: $primary;
        background: $panel;
    }

    ProgressBar > .bar--complete {
        color: $success;
    }

    /* Invite de commande type Claude Code / AGY sans encadré */
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
        ("q", "quit", "Quitter"),
        ("ctrl+c", "quit", "Quitter"),
        ("t", "cycle_theme", "Changer Thème"),
        ("r", "refresh", "Rafraîchir"),
        ("s", "summary", "Export Summary"),
        ("c", "focus_chat", "Prompt Agent"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield TopStatusBanner()
        
        with VerticalScroll(id="grid-container"):
            with Grid(id="main-grid"):
                with Vertical():
                    yield Label("❯ AGENTS ACTIFS", classes="pane-title")
                    yield AgentCard("Claude Code", "Root", "Refactoring board.py", "04m 12s", "running")
                    yield AgentCard("agy", "Gemini 3.6", "Writing unit tests", "01m 45s", "running")
                
                yield TokenGauges()
                yield GitStatusPane()
                yield SecurityAuditPane()
                yield TestPerfPane()
                yield TimelinePane()

        yield AgentPromptBar()
        yield Footer()

    def on_resize(self, event) -> None:
        """Ajuste dynamiquement la grille en 1 ou 2 colonnes selon la largeur du terminal."""
        try:
            grid = self.query_one("#main-grid", Grid)
            if event.size.width < 100:
                grid.styles.grid_size_columns = 1
            else:
                grid.styles.grid_size_columns = 2
        except Exception:
            pass

    def action_cycle_theme(self) -> None:
        """Cycle dynamiquement entre les thèmes agents de code."""
        self.current_theme_index = (self.current_theme_index + 1) % len(self.THEMES_CYCLE)
        new_theme = self.THEMES_CYCLE[self.current_theme_index]
        self.theme = new_theme
        self.notify(f"🎨 Thème actif : [bold primary]{new_theme}[/bold primary]", title="Agent Theme Switcher")

    def action_focus_chat(self) -> None:
        """Focus sur l'input du prompt agent."""
        chat_input = self.query_one("#chat-input", Input)
        chat_input.focus()

if __name__ == "__main__":
    app = SentinelApp()
    app.run()
