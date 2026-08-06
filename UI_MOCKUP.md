# 🎨 Sentinel CLI — UI Mockup & Terminal Layout Specification

> **Note sur le rendu visuel :** Les schémas ci-dessous sont des fils de fer ASCII (wireframes). Le rendu réel à l'exécution est géré par **Textual** (Flexbox, CSS Terminal) et **Rich** (TrueColor 16,7M de couleurs, dégradés, thèmes sombres/néon, bordures arrondies et interactivité complète à la souris).

```text
╭─────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ 🛡️  SENTINEL CLI v1.0 — DASHBOARD SYSTEM  │  Project: SENTINEL             │  LLM: x99 (Ollama Qwen32B)    │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

 🤖 AGENTS & SUB-AGENTS ACTIFS                             💡 CONTEXTE & OPTIMISATION TOKENS
╭────────────────────────────────────────────────────────╮╭────────────────────────────────────────────────────╮
│ 🟢 [Pane #1] Claude Code (Root)                       ││ 📊 Context Window: [████████████░░░░] 68% (136k/200k)│
│    └─ Action: Refactoring `src/engine/board.py`        ││ 💰 Session Cost: $0.42 (~48k input, ~4k output)   │
│    └─ Elapsed: 04m 12s  │  Est. remaining: ~01m 30s   ││                                                    │
│                                                        ││ ⚠️  RECOMMANDATION CONTEXTE:                        │
│ 🟡 [Pane #2] agy (Sub-agent: Gemini 3.6 Flash)          ││    Exécuter `/compact` dans Pane #1 sous peu.      │
│    └─ Action: Writing unit tests for `movegen.py`      ││                                                    │
│    └─ Elapsed: 01m 45s  │  Tools: FileRead, PyTest     ││ 💡 CONSEILS OPTIMISATION TOKENS:                   │
│                                                        ││    • Activer le skill `local-file-picker` (-40% tok)│
│ 🛠️  MCPs Actifs: [sqlite] [github] [playwright]         ││    • Utiliser RAG Local sur `x99` pour docs C++    │
╰────────────────────────────────────────────────────────╯╰────────────────────────────────────────────────────╯

 📝 CODE & MODIFICATIONS EN DIRECT (Git)                  🛡️  AUDIT SÉCURITÉ & QUALITÉ IA (x99 Sentinelle)
╭────────────────────────────────────────────────────────╮╭────────────────────────────────────────────────────╮
│ Branch: `main`                    │  Status: 3 Modified││ 🟢 `src/engine/board.py`                           │
│ Stats:  +142 lines  │  -38 lines                       ││    └─ RAS: Code propre, typage C++ respecté.       │
│                                                        ││                                                    │
│ 📄 src/engine/board.py        (+98, -12)  [Modifié]  ││ ⚠️  `src/engine/eval.py` (Ligne 112)               │
│ 📄 tests/test_forcing_tree.py (+44, -26)  [Nouveau]  ││    └─ Attention: Risque d'index hors-limites       │
│ 📄 include/bitboard.hpp       (+0, -0)   [Staged]   ││       sur la boucle `transposition_table_lookup`.  │
│                                                        ││ 🔒 Sécurité: Aucune clé/secret détecté.            │
╰────────────────────────────────────────────────────────╯╰────────────────────────────────────────────────────╯

 🧪 TESTS, BUILD & PERFORMANCES MOTEUR                    📜 CHRONOLOGIE & JOURNAL DE SESSION
╭────────────────────────────────────────────────────────╮╭────────────────────────────────────────────────────╮
│ 🔨 Compilation: ✅ PASS (GCC 14 -O3 -flto, 0 warnings)  ││ 🕒 23:15:02 — Session démarrée                      │
│ 🧪 Tests Unitaires: 142/142 Passed (100%)              ││ 🕒 23:20:18 — Commit: "Add L4 forcing tree base"   │
│                                                        ││ 🕒 23:28:44 — Agent AGY: Tests unitaires générés  │
│ ⚡ BENCHMARK MOTEUR (36 Cœurs x99):                    ││ 🕒 23:35:10 — Sentinelle: Alerte perf résolue (+4%)│
│    • Speed: 14.8M NPS  (▲ +4.2% vs baseline)           ││                                                    │
│    • RAM: 1.2 GB / 64 GB  │  Threads: 18               ││ 📝 Taper `sentinel summary` pour exporter le log.  │
╰────────────────────────────────────────────────────────╯╰────────────────────────────────────────────────────╯

 [Q] Quitter   [C] Chat Projet   [R] Rafraîchir   [S] Export Summary   [O] Optimiser Tokens   [T] Lancer Tests
───────────────────────────────────────────────────────────────────────────────────────────────────────────────
```

---

## 🚀 Onboarding Wizard Mockup (`sentinel init`)

```text
╭─────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ 🛡️  SENTINEL CLI v1.0 — ASSISTANT DE CONFIGURATION INITIALE (`sentinel init`)                              │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

 🔍 1. AUTO-DÉTECTION DE L'ENVIRONNEMENT IA & CLI
 ╭────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
 │  ✅ CLI Claude Code (`claude`)  : Trouvé dans /usr/local/bin/claude                                         │
 │  ✅ CLI AGY (`agy`)             : Trouvé dans ~/.gemini/bin/agy                                            │
 │  ✅ Serveur Local Ollama        : Détecté sur http://127.0.0.1:11434 (Modèle: `qwen2.5-coder:32b`)           │
 ╰────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

 🎯 2. SÉLECTION DU LLM SENTINELLE PRINCIPAL (Sélectionnez avec [▲/▼] et validez avec [Entrée])
 ╭────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
 │  🟢 [x] Local x99 (Ollama HTTP)  ── model: qwen2.5-coder:32b  (Latence: 45ms - Gratuit)                   │
 │  ⚪ [ ] Gemini 3.6 Flash (AGY)   ── command: `agy -p`          (Latence: 320ms - Faible coût)                │
 │  ⚪ [ ] Claude Code (Subprocess) ── command: `claude -p`       (Latence: 450ms - Élevé)                     │
 ╰────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

 📁 3. AUTO-DÉTECTION DU PROJET & CONFIGURATION DES TESTS
 ╭────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
 │  • Projet détecté  : C++ / Python (Dossier courant: `/SENTINEL`)                                           │
 │  • Commande de test: `pytest`  [Modifier]                                                                 │
 │  • Scanner de clé  : ✅ Activé (API keys, SSH keys, AWS secrets)                                          │
 ╰────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

 💾 Fichiers de configuration générés:
    - Global: ~/.config/sentinel/config.json
    - Projet: .sentinel.json

 [Valider & Lancer Dashboard]                              [Annuler]

