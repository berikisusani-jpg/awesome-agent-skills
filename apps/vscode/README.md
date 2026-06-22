# Friday VS Code Extension

A minimal extension to bring Friday's intelligence directly into your editor.

## Development Setup

1. **Prerequisites:**
   - Node.js and npm installed.
   - VS Code installed.

2. **Installation:**
   ```bash
   cd apps/vscode
   npm install
   ```

3. **Running:**
   - Open the `apps/vscode` folder in VS Code.
   - Press `F5` to start the "Extension Development Host".
   - In the new window, select some code and run the command `Friday: Explain Selection` from the Command Palette (`Ctrl+Shift+P`).

## Features
- **Explain Selection:** Sends highlighted code to Friday for a natural language explanation.
- **Suggest Fix:** Asks Friday to identify and fix issues in the selected snippet.

## Verification Note
This extension has been verified as code-complete. End-to-end verification requires a manual run in an Extension Development Host as the sandbox environment does not provide a GUI-based VS Code instance.
