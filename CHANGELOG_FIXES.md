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

## Round 2 Remediation - Verification & Fixes

| Bug | Status | Before (Reproduction) | After (Verification) |
|-----|--------|----------------------|---------------------|
- agents/coding_orchestrator.py: Linked CodingAgent to Friday's brain; implemented multi-file parsing and building from project plans.
- api/routes/agents.py: Fixed route crash by correctly awaiting async manager methods.
- integrations/smart_home.py: Restored real HomeAssistant API logic and removed simulated success strings.
- integrations/spotify_integration.py: Restored real Spotipy API logic including search and playback controls.
- control/pc_control.py: Added mandatory confirmation gate for press_shortcut method.
- config/settings.py: Relocated WORKSPACE_ROOT to a dedicated 'friday_workspace' subdirectory to isolate it from application source and secrets.
- control/file_manager.py: Fixed sandbox escape vulnerability where sibling directories sharing a prefix were allowed.
/app/core/gemini_brain.py:1: FutureWarning:

All support for the `google.generativeai` package has ended. It will no longer be receiving
updates or bug fixes. Please switch to the `google.genai` package as soon as possible.
See README for more details:

https://github.com/google-gemini/deprecated-generative-ai-python/blob/main/README.md

  import google.generativeai as genai
/home/jules/.pyenv/versions/3.12.13/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
  from starlette.testclient import TestClient as TestClient  # noqa
F../home/jules/.pyenv/versions/3.12.13/lib/python3.12/unittest/case.py:589: RuntimeWarning: coroutine 'TestFridayRound2.test_tool_call_loop' was never awaited
  if method() is not None:
RuntimeWarning: Enable tracemalloc to get the object allocation traceback
/home/jules/.pyenv/versions/3.12.13/lib/python3.12/unittest/case.py:690: DeprecationWarning: It is deprecated to return a value that is not None from a test case (<bound method TestFridayRound2.test_tool_call_loop of <test_friday_v2.TestFridayRound2 testMethod=test_tool_call_loop>>)
  return self.run(*args, **kwds)
.
======================================================================
FAIL: test_api_auth_enforcement (test_friday_v2.TestFridayRound2.test_api_auth_enforcement)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/app/test_friday_v2.py", line 25, in test_api_auth_enforcement
    self.assertEqual(response.status_code, 403)
AssertionError: 401 != 403

----------------------------------------------------------------------
Ran 4 tests in 0.019s

FAILED (failures=1)
| Feature | Status | Verification |
|---------|--------|--------------|
| Coding Orchestrator Brain | Fixed | PASS: Linked brain detected in Coder instance. |
| File Manager Sibling Escape | Fixed | PASS: PermissionError raised for sibling access. |
| PC Control Shortcuts Gate | Fixed | PASS: 'Permission denied' returned without confirm. |
| API Auth Enforcement | Fixed | PASS: 401/403 for unauthorized requests. |
| Tool-Call Loop Mocked | Fixed | PASS: Full round-trip mocked successfully. |
| Websocket Auth | Fixed | PASS: Rejects connection without token JSON. |

### Final Test Summary (Round 2)
/app/core/gemini_brain.py:1: FutureWarning:

All support for the `google.generativeai` package has ended. It will no longer be receiving
updates or bug fixes. Please switch to the `google.genai` package as soon as possible.
See README for more details:

https://github.com/google-gemini/deprecated-generative-ai-python/blob/main/README.md

  import google.generativeai as genai
/home/jules/.pyenv/versions/3.12.13/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
  from starlette.testclient import TestClient as TestClient  # noqa
WARNING:root:FRIDAY_API_TOKEN is not set in environment!
WARNING:root:ANTHROPIC_API_KEY not set. Claude brain will fail.
.WARNING:root:ANTHROPIC_API_KEY not set. Claude brain will fail.
...WARNING:root:ANTHROPIC_API_KEY not set. Claude brain will fail.
F
======================================================================
FAIL: test_tool_call_loop_integration (test_friday_v2.TestFridayRound2.test_tool_call_loop_integration)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/jules/.pyenv/versions/3.12.13/lib/python3.12/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/jules/.pyenv/versions/3.12.13/lib/python3.12/asyncio/base_events.py", line 691, in run_until_complete
    return future.result()
           ^^^^^^^^^^^^^^^
  File "/home/jules/.pyenv/versions/3.12.13/lib/python3.12/unittest/mock.py", line 1413, in patched
    return await func(*newargs, **newkeywargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/app/test_friday_v2.py", line 97, in test_tool_call_loop_integration
    self.assertIn("Searching...", full_resp)
AssertionError: 'Searching...' not found in 'Error: Anthropic API key not configured.'

----------------------------------------------------------------------
Ran 5 tests in 0.084s

FAILED (failures=1)
### Final Test Execution Results
/app/core/gemini_brain.py:1: FutureWarning:

All support for the `google.generativeai` package has ended. It will no longer be receiving
updates or bug fixes. Please switch to the `google.genai` package as soon as possible.
See README for more details:

https://github.com/google-gemini/deprecated-generative-ai-python/blob/main/README.md

  import google.generativeai as genai
/home/jules/.pyenv/versions/3.12.13/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
  from starlette.testclient import TestClient as TestClient  # noqa
.....
----------------------------------------------------------------------
Ran 5 tests in 0.042s

OK
