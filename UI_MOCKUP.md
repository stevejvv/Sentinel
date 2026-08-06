# Sentinel CLI — UI Mockup & Terminal Layout Specification

> **Note sur le rendu visuel :** Les schémas ci-dessous sont des fils de fer ASCII (wireframes). Le rendu réel à l'exécution est géré par **Textual** (Flexbox, CSS Terminal) et **Rich** (TrueColor 16,7M de couleurs, thèmes sombres/épurés sans encadrés et interactivité complète).

```text
SENTINEL CLI v1.0 — DASHBOARD SYSTEM  │  Project: SENTINEL  │  Watchdog: Local x99 (Qwen 32B)

 ❯ ACTIVE AGENTS                                           ❯ CONTEXT & TOKENS
   [RUNNING] Claude Code (Root)                              Context Window: [████████████░░░░] 68% (136k/200k)
   └─ Action: Refactoring src/engine/board.py                Session Cost: $0.42 (~48k input, ~4k output)
   └─ Elapsed: 04m 12s | Est: ~01m 30s                       [WARN] Recommendation: Run /compact

   [RUNNING] agy (Sub-agent: Gemini 3.6 Flash)             ❯ VERSION CONTROL (Git)
   └─ Action: Writing unit tests for movegen.py              Branch: main | Status: 3 Modified
   └─ Elapsed: 01m 45s | MCPs: sqlite, github               Diff: +142 -38 lines

 ❯ SECURITY & AUDIT                                        ❯ TESTS & PERFORMANCE
   [OK] src/engine/board.py (Clean)                          Build: [PASS] GCC 14 -O3
   [WARN] src/engine/eval.py (L112: Index check)             Tests: [PASS] 142/142 Passed
   [OK] Secrets: No API keys leaked                          Speed: 14.8M NPS (+4.2%)

 ❯ TIMELINE
   23:15 Session initialized
   23:20 Commit 'Add L4 tree'
   23:35 Performance alert resolved

 ❯ Ask a question, run a command (/compact, /clear)...
───────────────────────────────────────────────────────────────────────────────────────────────────────────────
```

---

## Onboarding Wizard Mockup (`sentinel init`)

```text
SENTINEL CLI v1.0 — ASSISTANT DE CONFIGURATION INITIALE (sentinel init)

 1. AUTO-DÉTECTION DE L'ENVIRONNEMENT IA & CLI
    [OK] CLI Claude Code (`claude`)  : Trouvé dans /usr/local/bin/claude
    [OK] CLI AGY (`agy`)             : Trouvé dans ~/.gemini/bin/agy
    [OK] Serveur Local Ollama        : Détecté sur http://127.0.0.1:11434 (Modèle: qwen2.5-coder:32b)

 2. SÉLECTION DU LLM SENTINELLE PRINCIPAL (Sélectionnez avec [▲/▼] et validez avec [Entrée])
    [x] Local x99 (Ollama HTTP)  ── model: qwen2.5-coder:32b  (Latence: 45ms - Gratuit)
    [ ] Gemini 3.6 Flash (AGY)   ── command: agy -p           (Latence: 320ms - Faible coût)
    [ ] Claude Code (Subprocess) ── command: claude -p        (Latence: 450ms - Élevé)

 3. AUTO-DÉTECTION DU PROJET & CONFIGURATION DES TESTS
    • Projet détecté  : C++ / Python (Dossier courant: /SENTINEL)
    • Commande de test: pytest  [Modifier]
    • Scanner de clé  : [OK] Activé (API keys, SSH keys, AWS secrets)

 Fichiers de configuration générés:
    - Global: ~/.config/sentinel/config.json
    - Projet: .sentinel.json

 [Valider & Lancer Dashboard]                              [Annuler]
