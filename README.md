# Project FRIDAY

FRIDAY (Fully Responsive Intelligent Digital Assistant Youth) is an advanced personal AI assistant focused on desktop automation, research, and integrated service management.

## ⚠️ PRODUCTION-GRADE NOTICE
This repository has undergone a final stability and production pass. All "God-Mode" or "Singularity" inflated features have been removed or converted into safe, human-reviewed protocols.

## Definitive Integration & Feature Table

| Feature / Integration | Status | Description |
|-----------------------|--------|-------------|
| **Core Brain** | Real | Powered by Claude 3 Opus with local fallback capabilities. |
| **Action Ledger** | Real | Human-in-the-loop approval system for sensitive actions. |
| **Ethical Sentinel** | Real | Automated screening of actions before queuing. |
| **Plugin System** | Real | Automatic discovery of integrations in `integrations/`. |
| **Gmail / Calendar** | Real | Authenticated API access for communication and scheduling. |
| **Spotify** | Real | Real search and playback control via Spotipy. |
| **Smart Home** | Real | HomeAssistant API integration for IoT control. |
| **Voice (STT/TTS)** | Real | OpenAI Whisper + ElevenLabs integration. |
| **Vision (OCR)** | Real | Screen analysis using Pytesseract and MSS. |
| **PC/Browser Control** | Real | PyAutoGUI and Playwright based automation. |
| **Self-Improvement** | Demo | `RecursiveModificationProtocol` generates proposals only. |
| **Life Synthesis** | Real | Synthesizes weather and news into personalized advice. |
| **Mobile App** | Roadmap | React Native skeleton exists but not fully wired. |
| **Multi-Tenancy** | Roadmap | Currently single-user focus only. |

## Installation
1. Clone the repository.
2. Run `pip install -r requirements.txt`.
3. Configure your `.env` based on `.env.example`.
4. Run `python main.py`.

## Infrastructure
- **CI**: GitHub Actions workflow for testing and smoke-booting.
- **Monitoring**: Structured JSON logging and `/healthz` endpoints.
- **Security**: Rate limiting on chat routes; Sentinel-screened action ledger.

See `docs/LIMITATIONS.md` for architectural boundaries.
