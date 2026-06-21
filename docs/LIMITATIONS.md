# Friday System Limitations

Friday is designed as a personal AI assistant for a single user in a local environment.

## 1. Single User Architecture
- **In-Memory History:** Conversation history is currently managed in-memory within the `FridayBrain` instance. Multi-user concurrent sessions will overwrite each other's context unless routed to unique brain instances.
- **Local Workspace:** `FileManager` and `PCControl` operate on the host machine's filesystem and display. There is no isolation between multiple API users.

## 2. Resource Constraints
- **Vision Capture:** Real-time screen analysis is token-intensive and may incur significant latency and cost if left in "always-on" mode.
- **Local TTS/STT:** Fallback engines (pyttsx3) depend on host OS drivers (e.g., eSpeak/SAPI5). If these are missing, voice output will fail.

## 3. Security Boundaries
- **No Sandboxing:** Code executed by the `CodingAgent` runs with the permissions of the `Friday` process. Use with caution in production environments.
- **Bearer Token:** The system uses a single static `FRIDAY_API_TOKEN`. It does not currently support granular user-based IAM or rotating keys.

## 4. Multi-monitor Support
- `PCControl` and `ScreenReader` primarily target the primary monitor. Coordinate mapping for secondary or tertiary displays is currently experimental.
