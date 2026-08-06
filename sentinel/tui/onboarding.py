import questionary
from rich.console import Console
from rich.panel import Panel
from sentinel.config import load_config, save_global_config, save_local_config

console = Console()

def run_onboarding_wizard():
    """Assistant d'onboarding interactif utilisant questionary et rich sans émojis."""
    console.print(Panel.fit("[bold cyan]Sentinel CLI — Assistant de Configuration Initial (sentinel init)[/bold cyan]", border_style="cyan"))

    # 1. Sélection de l'adaptateur principal
    adapter_choice = questionary.select(
        "Sélectionnez le LLM principal pour Sentinel (Sentinelle, Doctor & Chat) :",
        choices=[
            "Ollama HTTP Local (qwen2.5-coder:32b sur http://127.0.0.1:11434)",
            "AGY CLI Subprocess (Gemini 3.6 Flash)",
            "Claude Code CLI Subprocess (claude -p)",
            "Configurer un adaptateur personnalisé"
        ]
    ).ask()

    # 2. Commande de test automatique
    test_cmd = questionary.text(
        "Quelle est la commande d'exécution des tests du projet ?",
        default="pytest"
    ).ask()

    # 3. Scanner de sécurité
    sec_scanner = questionary.confirm(
        "Activer la Sentinelle de Sécurité (interception des clés d'API et secrets Git) ?",
        default=True
    ).ask()

    console.print("\n[bold green][OK] Configuration terminée avec succès ![/bold green]")
    console.print("[dim]Fichiers enregistrés : ~/.config/sentinel/config.json et .sentinel.json[/dim]\n")
