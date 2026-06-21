# Project FRIDAY - Operational Limitations

This document outlines the current boundaries and design limitations of Project FRIDAY.

## 1. Single-User Design
FRIDAY is currently architected as a personal assistant for a single user.
- **Session Management**: Conversation history is stored in-memory (or locally) without robust multi-tenant isolation.
- **Resource Lock**: Only one action-execution flow can reliably control the host machine (keyboard/mouse) at a time.

## 2. Local Workspace Dependency
- **File System**: FRIDAY assumes a local `friday_workspace` for file operations. It is not designed to handle distributed file systems or multi-user file permissions.
- **Execution Context**: Code execution and tool usage happen in the context of the user running the `main.py` or the API server.

## 3. Single-Process Architecture
- **Concurrency**: While the backend is asynchronous, the actual execution of PC control actions (via `pyautogui`) is inherently sequential at the hardware level.
- **Scaling**: Scaling the API horizontally would not scale the agent's ability to control a single physical or virtual machine.

## 4. Security & Isolation
- **LLM Code Execution**: FRIDAY can generate and execute Python code. While there is an `EthicalSentinel` for basic screening, this should be run in an isolated environment (like a dedicated VM or Container) if used with high-privilege access.
- **Plaintext Environment**: Secrets are managed via `.env` files. In a true enterprise production environment, a secrets manager (e.g., Vault, AWS Secrets Manager) should be used.

## 5. Vision and UI
- **Screen Resolution**: Screen analysis is sensitive to resolution and scaling settings.
- **Accessibility**: FRIDAY relies on OCR and visual analysis; applications with complex custom shaders or non-standard UI frameworks may be less readable.
