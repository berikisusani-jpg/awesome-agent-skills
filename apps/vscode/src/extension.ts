import * as vscode from 'vscode';
import axios from 'axios';

export function activate(context: vscode.ExtensionContext) {
	console.log('Friday VS Code extension is now active!');

	let explainCommand = vscode.commands.registerCommand('friday.explain', async () => {
		const editor = vscode.window.activeTextEditor;
		if (editor) {
			const selection = editor.document.getText(editor.selection);
			if (selection) {
				await callFriday("Explain this selection: " + selection);
			} else {
				vscode.window.showInformationMessage("Please select some code first.");
			}
		}
	});

	let fixCommand = vscode.commands.registerCommand('friday.fix', async () => {
		const editor = vscode.window.activeTextEditor;
		if (editor) {
			const selection = editor.document.getText(editor.selection);
			if (selection) {
				await callFriday("Suggest a fix for this code: " + selection);
			}
		}
	});

	context.subscriptions.push(explainCommand, fixCommand);
}

async function callFriday(prompt: string) {
	const outputChannel = vscode.window.createOutputChannel("Friday AI");
	outputChannel.show();
	outputChannel.appendLine("Contacting Friday...");

	try {
		const token = process.env.FRIDAY_API_TOKEN || "dev_token";
		const response = await axios.post('http://localhost:8000/api/chat', {
			message: prompt
		}, {
			headers: { 'Authorization': `Bearer ${token}` }
		});

		outputChannel.appendLine("\n--- Friday's Response ---");
		outputChannel.appendLine(response.data.response);
	} catch (error: any) {
		outputChannel.appendLine("\nError contacting Friday: " + error.message);
	}
}

export function deactivate() {}
