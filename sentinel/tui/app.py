from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Label
from textual.containers import Container, Horizontal, Vertical

class AgentPane(Static):
    """Pane affichant les agents & sub-agents actifs."""
    def compose(self) -> ComposeResult:
        yield Label("🤖 AGENTS & SUB-AGENTS ACTIFS", classes="pane-title")
        yield Static("🟢 [Pane #1] Claude Code (Root)\n   └─ Action: Refactoring src/engine/board.py\n   └─ Elapsed: 04m 12s | Est: ~01m 30s\n\n🟡 [Pane #2] agy (Sub-agent: Gemini 3.6 Flash)\n   └─ Action: Writing unit tests for movegen.py", id="agent-list")

class TokenPane(Static):
    """Pane affichant la fenêtre de contexte et les conseils d'optimisation."""
    def compose(self) -> ComposeResult:
        yield Label("💡 CONTEXTE & OPTIMISATION TOKENS", classes="pane-title")
        yield Static("📊 Context Window: [████████████░░░░] 68% (136k/200k)\n💰 Session Cost: $0.42 (~48k input, ~4k output)\n\n⚠️ RECOMMANDATION:\n   Exécuter /compact dans Pane #1 sous peu.", id="token-info")

class GitPane(Static):
    """Pane affichant le statut Git et les modifications en direct."""
    def compose(self) -> ComposeResult:
        yield Label("📝 CODE & MODIFICATIONS GIT", classes="pane-title")
        yield Static("Branch: main | Status: 3 Modified (+142, -38)\n\n📄 src/engine/board.py (+98, -12)\n📄 tests/test_forcing_tree.py (+44, -26)", id="git-info")

class SecurityPane(Static):
    """Pane affichant l'audit de sécurité et qualité IA."""
    def compose(self) -> ComposeResult:
        yield Label("🛡️ AUDIT SÉCURITÉ (Sentinelle x99)", classes="pane-title")
        yield Static("🟢 src/engine/board.py: RAS\n⚠️ src/engine/eval.py (L112): Risque index hors-limite\n🔒 Sécurité: Aucune clé détectée", id="security-info")

class SentinelApp(App):
    """Application TUI principale Sentinel sous Textual."""

    CSS = """
    Screen {
        layout: grid;
        grid-size: 2 2;
        grid-gutter: 1;
        padding: 1;
        background: #0F172A;
    }

    Static {
        border: round #00F0FF;
        background: #1E293B;
        padding: 1;
        color: #E2E8F0;
    }

    .pane-title {
        color: #00F0FF;
        text-style: bold;
        border-bottom: solid #334155;
        margin-bottom: 1;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quitter"),
        ("r", "refresh", "Rafraîchir"),
        ("s", "summary", "Export Summary"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield AgentPane(id="agents")
        yield TokenPane(id="tokens")
        yield GitPane(id="git")
        yield SecurityPane(id="security")
        yield Footer()

if __name__ == "__main__":
    app = SentinelApp()
    app.run()
