from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Label, ProgressBar, Input, Button
from textual.containers import Vertical, Grid, Horizontal, VerticalScroll

from textual.theme import Theme

# Thème Herdr-Minimaliste sur mesure
HERDR_MINIMAL_THEME = Theme(
    name="herdr-minimal",
    primary="#38BDF8",       # Cyan Minimal Air
    secondary="#818CF8",     # Indigo Doux
    warning="#FBBF24",       # Amber Pastel
    error="#F87171",         # Coral Pastel
    success="#34D399",       # Émeraude Doux
    accent="#A78BFA",        # Lavande
    foreground="#F8FAFC",    # Blanc Cassé
    background="#0B0F17",    # Fond Ardoise Très Sombre & Épuré
    surface="#151D2A",       # Surface Panneaux
    panel="#1E293B",         # Bordures et éléments d'arrière-plan
    dark=True,
)

class TopStatusBanner(Static):
    """Bannière supérieure minimaliste type Herdr."""
    def compose(self) -> ComposeResult:
        yield Label("🛡️ SENTINEL  │  Projet: [bold]SENTINEL[/bold]  │  Sentinelle: [dim]Local x99 (Qwen 32B)[/dim]", id="banner-text")

class AgentCard(Static):
    """Carte d'agent minimaliste et aérée."""
    def __init__(self, agent_name: str, role: str, action: str, elapsed: str, status: str = "running", **kwargs):
        super().__init__(**kwargs)
        self.agent_name = agent_name
        self.role = role
        self.action = action
        self.elapsed = elapsed
        self.status = status

    def compose(self) -> ComposeResult:
        status_icon = "🟢" if self.status == "running" else "🟡"
        yield Label(f"{status_icon} [bold cyan]{self.agent_name}[/bold cyan] [dim]• {self.role}[/dim]")
        yield Label(f"   └─ [italic]{self.action}[/italic]")
        yield Label(f"   └─ Temps: [dim]{self.elapsed}[/dim]  │  MCPs: [yellow]sqlite, github[/yellow]")

class TokenGauges(Static):
    """Panneau de contexte et de consommation de tokens."""
    def compose(self) -> ComposeResult:
        yield Label("💡 CONTEXTE & TOKENS", classes="pane-title")
        yield Label("📊 Fenêtre: [bold cyan]68%[/bold cyan] [dim](136k / 200k tokens)[/dim]")
        pb = ProgressBar(total=100, show_eta=False, id="context-bar")
        pb.progress = 68
        yield pb
        yield Label("💰 Session: [bold green]$0.42[/bold green] [dim](48k input, 4k output)[/dim]")
        yield Label("\n⚠️ [yellow]Recommandation:[/yellow] Exécuter [cyan]/compact[/cyan] sous peu.")
        yield Label("\n💡 [magenta]Optimisation:[/magenta] Skill [dim]local-file-picker[/dim] (-40% tokens)")

class GitStatusPane(Static):
    """Statut Git minimaliste."""
    def compose(self) -> ComposeResult:
        yield Label("📝 VERSION CONTROL (Git)", classes="pane-title")
        yield Label("Branche: [bold cyan]main[/bold cyan]  │  Statut: [yellow]3 Modifiés[/yellow]")
        yield Label("Diff: [green]+142[/green] [red]-38[/red] lignes\n")
        yield Label("📄 [white]src/engine/board.py[/white]      [green]+98[/green], [red]-12[/red]")
        yield Label("📄 [white]tests/test_forcing.py[/white]    [green]+44[/green], [red]-26[/red]")
        yield Label("📄 [white]include/bitboard.hpp[/white]      [dim]+0, -0[/dim]")

class SecurityAuditPane(Static):
    """Audit de sécurité minimaliste."""
    def compose(self) -> ComposeResult:
        yield Label("🛡️ SÉCURITÉ & QUALITÉ", classes="pane-title")
        yield Label("🟢 [white]src/engine/board.py[/white] [dim]Code propre[/dim]")
        yield Label("\n⚠️ [yellow]src/engine/eval.py[/yellow] [dim]L112: Risque d'index[/dim]")
        yield Label("\n🔒 [green]Scanner Secrets:[/green] [dim]Aucune clé détectée[/dim]")

class TestPerfPane(Static):
    """Métriques de tests et perf."""
    def compose(self) -> ComposeResult:
        yield Label("🧪 TESTS & PERFORMANCES", classes="pane-title")
        yield Label("🔨 Compilation: [green]✅ PASS[/green]")
        yield Label("🧪 Tests Unitaires: [green]142/142 Passed[/green]\n")
        yield Label("⚡ Vitesse Moteur: [cyan]14.8M NPS[/cyan] [green](+4.2%)[/green]")
        yield Label("   RAM: [dim]1.2 GB / 64 GB[/dim]")

class TimelinePane(Static):
    """Chronologie de session."""
    def compose(self) -> ComposeResult:
        yield Label("📜 CHRONOLOGIE", classes="pane-title")
        yield Label("🕒 [dim]23:15[/dim] Session démarrée")
        yield Label("🕒 [dim]23:20[/dim] Commit: 'Add L4 forcing tree base'")
        yield Label("🕒 [dim]23:28[/dim] AGY: Tests générés")
        yield Label("🕒 [dim]23:35[/dim] Sentinelle: Alerte perf résolue")

class InteractiveChatBar(Horizontal):
    """Barre de chat minimaliste."""
    def compose(self) -> ComposeResult:
        yield Input(placeholder="💬 Posez une question au LLM ou tapez une commande (/compact, /clear)...", id="chat-input")
        yield Button("Envoyer", variant="primary", id="chat-send")

class SentinelApp(App):
    """Application TUI Minimaliste Herdr-style avec Sélecteur de Thème dynamique."""

    TITLE = "Sentinel CLI"
    SUB_TITLE = "AI Watchdog & Minimalist Dashboard"

    # Liste des thèmes cyclables
    THEMES_CYCLE = ["herdr-minimal", "tokyo-night", "nord", "catppuccin-latte", "dracula", "rose-pine"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_theme(HERDR_MINIMAL_THEME)
        self.theme = "herdr-minimal"
        self.current_theme_index = 0

    CSS = """
    Screen {
        layout: vertical;
        padding: 0;
    }

    TopStatusBanner {
        background: $surface;
        color: $primary;
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
        grid-gutter: 1;
        padding: 1 2;
    }

    /* Media query réactive pour terminaux étroits (< 100 colonnes) */
    @media (max-width: 100) {
        #main-grid {
            grid-size: 1;
        }
    }


    Static {
        background: $surface;
        border: round $panel;
        padding: 1 2;
    }

    Static:focus {
        border: round $primary;
    }

    .pane-title {
        color: $primary;
        text-style: bold;
        border-bottom: solid $panel;
        margin-bottom: 1;
        padding-bottom: 0;
    }

    ProgressBar {
        margin-top: 1;
        margin-bottom: 1;
    }

    ProgressBar > .bar--bar {
        color: $primary;
        background: $panel;
    }

    ProgressBar > .bar--complete {
        color: $accent;
    }

    InteractiveChatBar {
        height: 3;
        padding: 0 2;
        background: $surface;
        border-top: solid $panel;
    }

    #chat-input {
        width: 1fr;
        border: round $panel;
        background: $background;
        color: $foreground;
    }

    #chat-send {
        width: 12;
        margin-left: 1;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quitter"),
        ("ctrl+c", "quit", "Quitter"),
        ("t", "cycle_theme", "Changer Thème"),
        ("r", "refresh", "Rafraîchir"),
        ("s", "summary", "Export Summary"),
        ("c", "focus_chat", "Chat Projet"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield TopStatusBanner()
        
        with VerticalScroll(id="grid-container"):
            with Grid(id="main-grid"):
                with Vertical():
                    yield Label("🤖 AGENTS & SUB-AGENTS ACTIFS", classes="pane-title")
                    yield AgentCard("Claude Code (Root)", "Root Agent", "Refactoring src/engine/board.py", "04m 12s", "running")
                    yield AgentCard("agy", "Sub-agent Gemini 3.6", "Writing unit tests for movegen.py", "01m 45s", "running")
                
                yield TokenGauges()
                yield GitStatusPane()
                yield SecurityAuditPane()
                yield TestPerfPane()
                yield TimelinePane()

        yield InteractiveChatBar()
        yield Footer()

    def action_cycle_theme(self) -> None:
        """Cycle dynamiquement entre les thèmes disponibles."""
        self.current_theme_index = (self.current_theme_index + 1) % len(self.THEMES_CYCLE)
        new_theme = self.THEMES_CYCLE[self.current_theme_index]
        self.theme = new_theme
        self.notify(f"🎨 Thème actif : [bold cyan]{new_theme}[/bold cyan]", title="Sélecteur de Thème")

    def action_focus_chat(self) -> None:
        """Focus sur le champ de saisie du chat interactif."""
        chat_input = self.query_one("#chat-input", Input)
        chat_input.focus()

if __name__ == "__main__":
    app = SentinelApp()
    app.run()

