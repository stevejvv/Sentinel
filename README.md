# Sentinel CLI — Terminal AI Watchdog & Agentic Dashboard

**Sentinel** est une CLI agnostique, modulaire et ultra-rapide conçue pour servir de **Tableau de Bord, Sentinelle de Sécurité et Conseiller d'Optimisation de Tokens** pour les sessions de développement assistées par des agents IA (Claude Code, AGY, OpenCode, etc.).

---

## Fonctionnalités Clés

1. **Orchestration & Monitoring d'Agents**
   - Suivi en temps réel des agents et sub-agents actifs (actions en cours, temps écoulé, estimation restante).
   - Suivi précis de la consommation de tokens et des coûts financiers de la session.
   - Inventaire dynamique des Skills, Serveurs MCP et Outils engagés par les agents.
   - **Indicateur de fenêtre de contexte** (avec alertes intelligentes pour exécuter `/compact` ou `/clear` avant saturation).
   - **Conseiller d'Optimisation de Tokens :** Recommandations d'installation de Skills/MCPs (RAG local, AST-grep, File Pickers) pour réduire de 50 à 80% l'usage de tokens.

2. **Répertoire, Git & Sécurité**
   - Tracking en temps réel des diffs Git (`+ / -` lignes, fichiers touchés).
   - **Sentinelle de Sécurité :** Interception automatique des fuites de clés d'API (`sk-...`, `AIza...`), tokens SSH/AWS ou failles de mémoire (C++/Python).

3. **Diagnostic, Langage, Perf & Tests**
   - **Docteur de compilation :** Traduction en 1 phrase claire des erreurs complexes de templates C++ ou tracebacks Python.
   - **Banc de tests automatisé :** Exécution en arrière-plan des tests (`pytest`, `ctest`, `cargo test`) avec détection de régressions.
   - **Monitoring de performances :** Suivi des métriques de vitesse (*NPS*, empreinte RAM, latence).

4. **Chronologie & Journal Automatique (`sentinel summary`)**
   - Historique chronologique des événements et génération automatique de rapports de dev en Markdown (Changelog).

5. **Chat & Assistant Projet (`sentinel chat`)**
   - Interface Q&A interactive basée sur vos adaptateurs LLM préférés (votre serveur local `x99` via Ollama, `claude -p`, `agy -p`, etc.).

6. **Onboarding & Assistant de Configuration (`sentinel init`)**
   - Wizard interactif avec auto-détection des CLI IA (`claude`, `agy`, `opencode`), ping d'Ollama local, détection du banc de tests du projet et génération de `~/.config/sentinel/config.json` / `.sentinel.json`.

---

## Structure du Projet

```text
SENTINEL/
├── README.md              # Présentation globale & installation
├── ARCHITECTURE.md        # Spécification technique, modules & onboarding
├── UI_MOCKUP.md           # Maquette TUI / Dashboard & Wizard d'onboarding
```

---

## Prochaines Étapes

1. Lancer la session AGY dans ce dossier.
2. Implémenter l'ossature Python du package `sentinel` (CLI & commande `sentinel init`).
3. Développer les adaptateurs LLM (CLI & Ollama) et le rendu TUI moderne avec `textual` & `rich`.
