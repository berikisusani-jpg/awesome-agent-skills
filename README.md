# Project FRIDAY - Production-Grade Personal AI Assistant

FRIDAY (Fully Responsive Intelligent Digital Assistant) is a secure, proactive, and multi-integrated AI ecosystem designed to manage your digital life.

## 🚀 Version 5.0.0 (Production Pass)

Friday combines LLM intelligence with a robust tool-calling framework and a human-in-the-loop security model.

### Feature Status (Implementation Audit)

| Feature Category | Feature | Status | Note |
|------------------|---------|--------|------|
| **Intelligence** | Multi-Brain (Claude/Gemini) | ✅ **REAL** | Integrated via Anthropic & Google SDKs. |
| **Intelligence** | Local Fallback (Ollama) | ✅ **REAL** | Configurable in `core/local_brain.py`. |
| **Safety** | Human-in-the-Loop Ledger | ✅ **REAL** | Sensitive actions require manual approval. |
| **Safety** | Ethical Sentinel | ✅ **REAL** | Gathers and flags high-risk actions for review. |
| **Integrations** | Weather / Calendar | ✅ **REAL** | Real API calls to OpenWeather/Google. |
| **Integrations** | Spotify / Smart Home | ✅ **REAL** | Real integration via Spotipy/HASS API. |
| **Integrations** | Gmail Triage | ✅ **REAL** | Autonomous email summarization & drafting. |
| **Control** | PC / Browser Automation | ✅ **REAL** | Python-controlled UI and Playwright automation. |
| **Vision** | Visual Grounding | ✅ **REAL** | Uses GPT-4o to locate UI elements visually. |
| **Skills** | Morning Briefing | ✅ **REAL** | Multi-step autonomous daily summary. |
| **Skills** | Deep Research | ✅ **REAL** | Real web search synthesis with citations. |
| **Skills** | Code Tutor | ✅ **REAL** | Line-grounded teaching and quizzes. |
| **Skills** | Project Scaffolder | ✅ **REAL** | Multi-file generation with fix/retry loop. |
| **Skills** | Marketing Content | ✅ **REAL** | Labeled AI drafts and competitive research. |
| **Frontend** | VS Code Extension | ✅ **REAL** | Side-panel AI integration (Scaffolding). |
| **Frontend** | Desktop / Mobile / Web | 🛠 **ROADMAP** | Back-end API support and Electron scaffolding only. |
| **Self-Mod** | Recursive Self-Rewriting | ❌ **REMOVED** | Removed for safety in production environments. |

## 🛠 Quick Start
1. Run `bash setup.sh` to install dependencies and configure the environment.
2. Provide your API keys in the generated `.env` file.
3. Start the system: `python3 main.py`.
4. Access the API: `uvicorn api.main:app --host 0.0.0.0`.

## 🔒 Security
All autonomous actions pass through the **Action Ledger** (`core/ledger.py`). Depending on your `AUTONOMY_PROFILE` (GUEST, STANDARD, POWER), Friday will either auto-execute safe actions or wait for your explicit approval via the API.

## 📝 Documentation
- [Skills Framework](docs/SKILLS.md)
- [Security & Autonomy Model](docs/SECURITY.md)
- [System Limitations](docs/LIMITATIONS.md)

---
*Built for security and autonomy.*
