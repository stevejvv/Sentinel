# Sentinel CLI — Spécifications Architecturales & Détaillées

## 1. Vue d'Ensemble des Adaptateurs Multi-LLM

Sentinel n'est pas verrouillé sur une API payante. Il s'appuie sur une couche d'**Adaptateurs CLI & HTTP** modulaire :

```json
{
  "llm_adapters": {
    "local_x99": {
      "type": "ollama_http",
      "url": "http://127.0.0.1:11434",
      "model": "qwen2.5-coder:32b"
    },
    "claude_cli": {
      "type": "subprocess",
      "command": "claude -p"
    },
    "gemini_cli": {
      "type": "subprocess",
      "command": "agy -p --model 'Gemini 3.6 Flash (High)'"
    },
    "opencode_cli": {
      "type": "subprocess",
      "command": "opencode run -m"
    }
  }
}
```

---

## 2. Découpage des 5 Modules Clés

### Module 1 : Agent & Token Dashboard
- **Herdr Socket / Process Inspector :** Écoute les sockets Herdr ou surveille les processus terminaux pour lister les agents actifs (`claude`, `agy`, `opencode`).
- **Token Accounting Engine :** Lit les métriques de tokens de la session et calcule l'empreinte financière.
- **Context Health Indicator :** Calcule le pourcentage de remplissage de la fenêtre de contexte et prévient avant saturation (`/compact` / `/clear`).
- **Token Optimization Advisor :** Analyse le profil du projet et recommande les Skills/MCPs appropriés pour diviser la facture par 2.

### Module 2 : Version Control & Guard
- **Git Diff Engine :** Analyse en temps réel les fichiers modifiés (`git status`, `git diff --stat`).
- **Security Scanner :** Regex & règles heuristiques pour bloquer l'exposition de clés API, secrets, injections SQL ou fuites mémoire C++.

### Module 3 : Language, Errors & Perf
- **Compiler Error Translator :** Intercepte les erreurs C++/Python et génère une explication courte en français.
- **Background Test Runner :** Exécute automatiquement `pytest`, `ctest` ou `cargo test` en tâche de fond.
- **Perf Watchdog :** Mesure les régressions de vitesse (*NPS* pour les échecs, latence API, mémoire).

### Module 4 : Session Timeline & Summary
- **Event Recorder :** Enregistre chaque événement marquant (commit, test passé, agent démarré).
- **Markdown Reporter :** Génère un rapport de dev structuré à la demande (`sentinel summary`).

### Module 5 : Project Chat & Assistant
- **Interactive Q&A Bar :** Posez des questions au LLM local ou distant directement dans le terminal.

---

## 3. Assistant d'Onboarding & Workflow de Configuration (`sentinel init`)

Sentinel propose une expérience d'onboarding interactive et guidée pour configurer l'environnement au 1er lancement ou via la commande `sentinel init`.

### Les 5 Étapes du Workflow d'Onboarding

1. **Auto-détection de l'Environnement IA :**
   - Inspection du `$PATH` pour trouver les CLI agents (`claude`, `agy`, `opencode`).
   - Ping HTTP du serveur Ollama local (`http://127.0.0.1:11434`) et listing des modèles disponibles.
2. **Choix du Cerveau Sentinelle & Chat :**
   - Sélection du modèle/adaptateur principal via un menu TUI interactif.
   - Test en direct du délai de réponse (ping/latency check).
3. **Analyse du Projet & Commandes de Test :**
   - Identification automatique du type de projet (Python/pytest, C++/CMake/CTest, Rust/Cargo, JS/TS/Vitest).
   - Validation de la commande d'exécution des tests en arrière-plan.
4. **Définition des Règles de Sécurité :**
   - Choix de la sensibilité du scanner de secrets (API Keys, tokens SSH, regex personnalisées).
5. **Écriture des Fichiers de Configuration & Healthcheck (`sentinel check`) :**
   - `~/.config/sentinel/config.json` (Configuration globale & adaptateurs)
   - `.sentinel.json` (Configuration spécifique au dépôt/projet courant)
   - Test de confirmation finale.

---

## 4. Framework TUI & Design System (`Textual` + `Rich`)

Pour offrir une expérience visuelle épurée, fluide et haut de gamme, l'interface utilisateur de Sentinel repose sur l'écosystème **Textualize** :

### Stack Graphique
- **`Textual` (Framework TUI) :**
  - Architecture réactive événementielle (widgets, événements clavier/souris).
  - Disposition par **Flexbox & CSS Terminal** (TSS - Textual CSS).
  - Support natif du défilement, du redimensionnement fluide et de la souris.
- **`Rich` (Engine de Rendu) :**
  - Rendu TrueColor (16,7M de couleurs), typographie épurée.
  - Coloration syntaxique du code source et rendu Markdown en temps réel.
- **`Questionary` / `InquirerPy` :**
  - Prompting interactif pour l'onboarding (`sentinel init`) avec navigation au clavier.

### Charte Graphique & Palette Pro Code Agent
- **Thèmes Pro :** `claude-dark`, `herdr-dark`, `opencode-dark`, `matrix-geek`, `monokai-pro`.
