from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Label, ProgressBar, Input
from textual.containers import Vertical, Grid, Horizontal, VerticalScroll
from textual.theme import Theme

# Thème Geek Hi-Tech Épuré (Sans encadrés, style Claude Code / AGY / OpenCode)
HI_TECH_GEEK_THEME = Theme(
    name="hi-tech-geek",
    primary="#00F0FF",       # Cyan Néon Électrique
    secondary="#7000FF",     # Violet Synthwave
    warning="#FFB000",       # Amber Lumineux
    error="#FF453A",         # Rouge néon
    success="#00FF66",       # Vert Émeraude Matrix
    accent="#00F0FF",
    foreground="#E6EDF3",    # Texte très net (GitHub Dark style)
    background="#0D1117",    # Fond ultra-sombre geek
    surface="#161B22",       # Surface minimale
    panel="#21262D",         # Séparateurs subtils
    dark=True,
)

class TopStatusBanner(Static):
    """Bannière minimale sans bordures type CLI agent."""
    def compose(self) -> ComposeResult:
        yield Label("🛡️ [bold cyan]SENTINEL[/bold cyan] [dim]v0.1.0[/dim]  │  [dim]Project:[/dim] [bold white]SENTINEL[/bold white]  │  [dim]Watchdog:[/dim] [bold green]Local x99 (Qwen 32B)[/bold green]", id="banner-text")

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
        yield Label(f"   [dim]└─[/dim] Action: [cyan]{self.action}[/cyan]")
        yield Label(f"   [dim]└─ Elapsed:[/dim] [green]{self.elapsed}[/green]  │  [dim]MCPs:[/dim] [yellow]sqlite, github[/yellow]")

class TokenGauges(Static):
    """Panneau de contexte minimaliste sans encadré."""
    def compose(self) -> ComposeResult:
        yield Label("❯ FENÊTRE DE CONTEXTE & TOKENS", classes="pane-title")
        yield Label("📊 Contexte: [bold cyan]68%[/bold cyan] [dim](136k / 200k tokens)[/dim]")
        pb = ProgressBar(total=100, show_eta=False, id="context-bar")
        pb.progress = 68
        yield pb
        yield Label("💰 Session: [bold green]$0.42[/bold green] [dim](48k in, 4k out)[/dim]")
        yield Label("⚠️ [yellow]Rec:[/yellow] Exécuter [cyan]/compact[/cyan]")

class GitStatusPane(Static):
    """Statut Git épuré."""
    def compose(self) -> ComposeResult:
        yield Label("❯ VERSION CONTROL (Git)", classes="pane-title")
        yield Label("Branch: [bold cyan]main[/bold cyan]  │  [yellow]3 Modified[/yellow]")
        yield Label("Diff: [bold green]+142[/bold green] [bold red]-38[/bold red] lines")
        yield Label("📄 [white]src/engine/board.py[/white]      [green]+98[/green] [red]-12[/red]")
        yield Label("📄 [white]tests/test_forcing.py[/white]    [green]+44[/green] [red]-26[/red]")

class SecurityAuditPane(Static):
    """Audit de sécurité épuré."""
    def compose(self) -> ComposeResult:
        yield Label("❯ SÉCURITÉ & SENTINELLE", classes="pane-title")
        yield Label("🟢 [white]src/engine/board.py[/white] [dim]Clean[/dim]")
        yield Label("⚠️ [yellow]src/engine/eval.py[/yellow] [dim]L112: Index check[/dim]")
        yield Label("🔒 [green]Secrets:[/green] [dim]No API keys leaked[/dim]")

class TestPerfPane(Static):
    """Métriques de tests et perf épurées."""
    def compose(self) -> ComposeResult:
        yield Label("❯ TESTS & PERFORMANCES", classes="pane-title")
        yield Label("🔨 Build: [bold green]PASS (GCC 14 -O3)[/bold green]")
        yield Label("🧪 Tests: [bold green]142/142 Passed[/bold green]")
        yield Label("⚡ Speed: [bold cyan]14.8M NPS[/bold cyan] [green](+4.2%)[/green]")

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
    """Application TUI Geek & Hi-Tech sans encadrés, style Claude Code / AGY."""

    TITLE = "Sentinel CLI"
    SUB_TITLE = "Terminal AI Watchdog"

    THEMES_CYCLE = ["hi-tech-geek", "tokyo-night", "nord", "catppuccin-latte", "dracula", "rose-pine"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_theme(HI_TECH_GEEK_THEME)
        self.theme = "hi-tech-geek"
        self.current_theme_index = 0

    CSS = """
    Screen {
        layout: vertical;
        padding: 0;
        background: #0D1117;
    }

    TopStatusBanner {
        background: #161B22;
        color: #00F0FF;
        border: none;
        border-bottom: solid #21262D;
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
        background: #0D1117;
        border: none;
        border-left: solid #21262D;
        padding: 0 1;
    }

    Static:focus {
        border-left: solid #00F0FF;
    }

    .pane-title {
        color: #00F0FF;
        text-style: bold;
        border: none;
        border-bottom: solid #21262D;
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
        color: #00F0FF;
        background: #21262D;
    }

    ProgressBar > .bar--complete {
        color: #00FF66;
    }

    /* Invite de commande type Claude Code / AGY sans encadré */
    AgentPromptBar {
        height: 3;
        padding: 0 2;
        background: #161B22;
        border-top: solid #21262D;
        align: left middle;
    }

    #prompt-symbol {
        color: #00F0FF;
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
        color: #E6EDF3;
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
        """Cycle dynamiquement entre les thèmes disponibles."""
        self.current_theme_index = (self.current_theme_index + 1) % len(self.THEMES_CYCLE)
        new_theme = self.THEMES_CYCLE[self.current_theme_index]
        self.theme = new_theme
        self.notify(f"🎨 Thème actif : [bold cyan]{new_theme}[/bold cyan]", title="Sélecteur de Thème")

    def action_focus_chat(self) -> None:
        """Focus sur l'input du prompt agent."""
        chat_input = self.query_one("#chat-input", Input)
        chat_input.focus()

if __name__ == "__main__":
    app = SentinelApp()
    app.run()
