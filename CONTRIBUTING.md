# 🤝 Contributing to Sentinel CLI

Thank you for your interest in contributing to **Sentinel CLI**! 🛡️

Sentinel is an agnostic, fast, and modular Terminal AI Watchdog & Agentic Dashboard built for developer sessions powered by AI Coding Agents (Claude Code, AGY, OpenCode, Ollama, etc.).

## 🚀 Getting Started

1. **Fork & Clone the repository:**
   ```bash
   git clone https://github.com/stevejvv/sentinel.git
   cd sentinel
   ```

2. **Set up a Virtual Environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -e .
   ```

3. **Run Sentinel in Development Mode:**
   ```bash
   sentinel init
   sentinel
   ```

## 🛠️ Architecture & Stack

- **TUI Framework:** [Textual](https://textual.textualize.io/)
- **Text & Syntax Rendering:** [Rich](https://rich.readthedocs.io/)
- **CLI Framework:** [Typer](https://typer.tiangolo.com/)
- **HTTP Client:** [HTTPX](https://www.python-httpx.org/)

Please read [ARCHITECTURE.md](ARCHITECTURE.md) and [UI_MOCKUP.md](UI_MOCKUP.md) for deeper technical specifications.

## 📜 License

By contributing to Sentinel, you agree that your contributions will be licensed under the [MIT License](LICENSE).
