from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Label, ProgressBar, Input, TabbedContent, TabPane, Button
from textual.containers import Container, Horizontal, Vertical, Grid, ScrollableContainer
from rich.text import Text
from rich.panel import Panel

class TopStatusBanner(Static):
    """Bannière supérieure affichant l'en-tête du système, le projet et le modèle actif."""
    def compose(self) -> ComposeResult:
        yield Label("🛡️  SENTINEL CLI v0.1.0  │  Projet: SENTINEL  │  Sentinelle: Local x99 (Qwen 32B)", id="banner-text")

class AgentCard(Static):
    """Carte individuelle d'agent actif."""
    def __init__(self, agent_name: str, role: str, action: str, elapsed: str, status: str = "running", **kwargs):
        super().__init__(**kwargs)
        self.agent_name = agent_name
        self.role = role
        self.action = action
        self.elapsed = elapsed
        self.status = status

    def compose(self) -> ComposeResult:
        status_icon = "🟢" if self.status == "running" else "🟡"
        yield Label(f"{status_icon} [bold cyan]{self.agent_name}[/bold cyan] [dim]({self.role})[/dim]")
        yield Label(f"   └─ Action: [italic]{self.action}[/italic]")
        yield Label(f"   └─ Temps écoulé: [green]{self.elapsed}[/green]  │  MCPs: [bold yellow][sqlite] [github][/bold yellow]")


class TokenGauges(Static):
    """Barres de jauge de consommation de tokens et de coût."""
    def compose(self) -> ComposeResult:
        yield Label("💡 FENÊTRE DE CONTEXTE & TOKENS", classes="pane-title")
        yield Label("📊 Fenêtre de contexte: [bold cyan]68%[/bold cyan] (136k / 200k tokens)")
        yield ProgressBar(total=100, completed=68, show_eta=False, id="context-bar")
        yield Label("💰 Coût estimé session: [bold green]$0.42[/bold green] (~48k input, ~4k output)")
        yield Label("\n⚠️ [bold yellow]ALERTE CONTEXTE:[/bold yellow]\n   Exécuter [bold cyan]/compact[/bold cyan] dans l'agent principal sous peu.")
        yield Label("\n💡 [bold magenta]CONSEILS D'OPTIMISATION:[/bold magenta]\n   • Activer le skill [bold white]`local-file-picker`[/bold white] (-40% tokens)\n   • Activer RAG Local sur `x99` pour docs C++")

class GitStatusPane(Static):
    """Pane affichant les statistiques Git en direct."""
    def compose(self) -> ComposeResult:
        yield Label("📝 CONTRÔLE DE VERSION (Git)", classes="pane-title")
        yield Label("Branche: [bold cyan]main[/bold cyan]  │  Statut: [bold yellow]3 Fichiers modifiés[/bold yellow]")
        yield Label("Diff: [bold green]+142 Lignes[/bold green]  │  [bold red]-38 Lignes[/bold red]\n")
        yield Label("📄 [bold white]src/engine/board.py[/bold white]       [green]+98[/green], [red]-12[/red]  [Modifié]")
        yield Label("📄 [bold white]tests/test_forcing.py[/bold white]     [green]+44[/green], [red]-26[/red]  [Nouveau]")
        yield Label("📄 [bold white]include/bitboard.hpp[/bold white]       [dim]+0, -0   [Staged][/dim]")

class SecurityAuditPane(Static):
    """Pane d'audit de sécurité et de qualité du code."""
    def compose(self) -> ComposeResult:
        yield Label("🛡️ AUDIT SÉCURITÉ & SENTINELLE IA", classes="pane-title")
        yield Label("🟢 [bold white]src/engine/board.py[/bold white]\n   └─ [dim]Code propre, typage C++ respecté.[/dim]")
        yield Label("\n⚠️ [bold yellow]src/engine/eval.py[/bold yellow] [dim](Ligne 112)[/dim]\n   └─ [yellow]Risque d'index hors-limite sur la boucle lookup.[/yellow]")
        yield Label("\n🔒 [bold green]Scanner de Clés:[/bold green] Aucune clé API ni secret détecté dans le stage.")

class TestPerfPane(Static):
    """Pane des résultats de tests et métriques de performance."""
    def compose(self) -> ComposeResult:
        yield Label("🧪 TESTS & PERFORMANCES MOTEUR", classes="pane-title")
        yield Label("🔨 Compilation: [bold green]✅ PASS (GCC 14 -O3 -flto, 0 warnings)[/bold green]")
        yield Label("🧪 Tests Unitaires: [bold green]142/142 Passed (100%)[/bold green]\n")
        yield Label("⚡ BENCHMARK MOTEUR (36 Cœurs x99):")
        yield Label("   • Vitesse: [bold cyan]14.8M NPS[/bold cyan] [green](▲ +4.2% vs baseline)[/green]")
        yield Label("   • Mémoire: [bold white]1.2 GB / 64 GB[/bold white]  │  Threads: [bold white]18[/bold white]")

class TimelinePane(Static):
    """Pane chronologique des événements de session."""
    def compose(self) -> ComposeResult:
        yield Label("📜 CHRONOLOGIE DE SESSION", classes="pane-title")
        yield Label("🕒 [dim]23:15:02[/dim] — Session démarrée")
        yield Label("🕒 [dim]23:20:18[/dim] — Commit: [italic]'Add L4 forcing tree base'[/italic]")
        yield Label("🕒 [dim]23:28:44[/dim] — Agent AGY: Tests unitaires générés")
        yield Label("🕒 [dim]23:35:10[/dim] — Sentinelle: Alerte perf résolue (+4%)")
        yield Label("\n📝 [dim]Taper [bold white]sentinel summary[/bold white] pour exporter le log.[/dim]")

class InteractiveChatBar(Horizontal):
    """Barre de chat et questions-réponses interactives."""
    def compose(self) -> ComposeResult:
        yield Input(placeholder="💬 Posez une question au LLM ou tapez une commande (/compact, /clear)...", id="chat-input")
        yield Button("Envoyer", variant="primary", id="chat-send")

class SentinelApp(App):
    """Application TUI principale Sentinel réécrite sous Textual avec Design System avancé."""

    TITLE = "Sentinel CLI — AI Watchdog Dashboard"
    SUB_TITLE = "Terminal Security Guard & Token Advisor"

    CSS = """
    Screen {
        background: #0B0F19;
        color: #F1F5F9;
        layout: vertical;
    }

    TopStatusBanner {
        background: #0F172A;
        color: #38BDF8;
        border-bottom: heavy #38BDF8;
        height: 3;
        content-align: center middle;
        text-style: bold;
    }

    #main-grid {
        layout: grid;
        grid-size: 2 3;
        grid-gutter: 1;
        padding: 1;
        height: 1fr;
    }

    Static {
        background: #1E293B;
        border: round #334155;
        padding: 1;
    }

    Static:focus {
        border: round #38BDF8;
        background: #0F172A;
    }

    .pane-title {
        color: #38BDF8;
        text-style: bold;
        border-bottom: solid #334155;
        margin-bottom: 1;
        padding-bottom: 0;
    }

    ProgressBar {
        margin-top: 1;
        margin-bottom: 1;
    }

    ProgressBar > .bar--bar {
        color: #00F0FF;
        background: #334155;
    }

    ProgressBar > .bar--complete {
        color: #38BDF8;
    }

    InteractiveChatBar {
        height: 3;
        padding: 0 1;
        background: #0F172A;
        border-top: solid #334155;
    }

    #chat-input {
        width: 1fr;
        border: round #38BDF8;
        background: #1E293B;
        color: #F8FAFC;
    }

    #chat-send {
        width: 12;
        margin-left: 1;
        background: #0284C7;
        color: #FFFFFF;
        border: none;
    }

    #chat-send:hover {
        background: #0369A1;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quitter"),
        ("r", "refresh", "Rafraîchir"),
        ("s", "summary", "Export Summary"),
        ("c", "focus_chat", "Chat Projet"),
        ("t", "run_tests", "Lancer Tests"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield TopStatusBanner()
        
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

    def action_focus_chat(self) -> None:
        """Focus sur le champ de saisie du chat interactif."""
        chat_input = self.query_one("#chat-input", Input)
        chat_input.focus()

if __name__ == "__main__":
    app = SentinelApp()
    app.run()
