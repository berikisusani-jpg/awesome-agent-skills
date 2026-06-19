# Changelog - Project FRIDAY Fixes

| ID | File | Change | Reason |
|----|------|--------|--------|
- api/routes/agents.py: Created missing route module.
- api/routes/integrations.py: Created missing route module.
- api/routes/chat.py: Fixed crash by lazily initializing FridayBrain.
- api/routes/memory.py: Fixed crash by lazily initializing FridayMemory; added 503 error on missing config.
- config/settings.py: Exposed all variables from .env.example.
- voice/speaker.py: Ported to ElevenLabs v1 SDK.
- setup.py: Fixed imports and ensured init_env() is called.
- voice/wake_word.py: Defaulted to 'bumblebee' (real keyword) and added support for custom .ppn path.
- vision/screen_analyzer.py: Updated to 'gpt-4o' model and added error handling for missing keys.
- core/brain.py: Updated Claude model to 'claude-3-5-sonnet-20240620' and added safety checks for API key.
- core/brain.py: Optimized multi-model routing and tool injection preparation.
- vision/screen_analyzer.py: Updated to GPT-4o for superior visual understanding.
- agents/agent_manager.py: Refined for tactical SWAT coordination.
- agents/: Unified all agent methods to be async.
- agents/tactical_manager.py: Fixed TypeError by properly awaiting async tasks in gather.
- integrations/crypto_tracker.py: Fixed missing price interpolation in f-string.
- vision/omniscient.py: Replaced blocking time.sleep with asyncio.sleep.
- core/proactive.py: Replaced blocking time.sleep with asyncio.sleep.
- core/brain.py: Implemented full tool-calling loop and history management (sliding window).
- apps/desktop/preload.js: Created missing preload script for Electron.
- apps/: Updated backend URLs to port 8000.
- core/universal_connector.py: Replaced fake success strings with real dispatch to integration classes; added honest 'not_implemented' status for others.
- integrations/smart_home.py: Wired to HomeAssistant API structure with token handling.
- integrations/spotify_integration.py: Wired to spotipy with OAuth flow preparation.
- vision/presence.py: Implemented real Haar cascade face detection using OpenCV.
- core/emotions.py: Improved detection to handle negation (e.g., 'not happy').
- agents/coding_agent.py: Now uses Friday's brain to generate real code from the prompt.
- agents/coding_orchestrator.py: Implemented real file writing to disk for project builds.
- control/file_manager.py: Implemented workspace root allow-listing, path normalization, and mandatory confirmation flags for all operations.
- control/pc_control.py: Added mandatory audit logging and confirmation gates for mouse/keyboard control.
- api/main.py: Restricted CORS to trusted origin and implemented HTTP Bearer authentication on all routes.
- control/browser_control.py: Added audit logging and mandatory confirmation gates.
- test_friday.py: Expanded test suite to cover emotions negation, crypto price fix, and file manager safety.
- core/: Re-audited all files for blocking calls; ensured asyncio.sleep usage everywhere.
- General: Verified uvicorn boots against placeholder .env without crash.
.....
----------------------------------------------------------------------
Ran 5 tests in 0.122s

OK
.....
----------------------------------------------------------------------
Ran 5 tests in 0.131s

OK
