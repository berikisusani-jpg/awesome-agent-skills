import asyncio
from control.app_launcher import AppLauncher
from control.pc_control import PCControl
from integrations.smart_home import SmartHomeIntegration

class WorkspaceOrchestrator:
    def __init__(self):
        self.launcher = AppLauncher()
        self.pc = PCControl()
        self.smarthome = SmartHomeIntegration()

    async def set_coding_mode(self):
        print("Friday: Setting up Coding Mode. Focus enabled.")
        self.smarthome.control_lights("dim")
        self.launcher.launch("VS Code")
        self.launcher.launch("Chrome")
        # Simulate window positioning
        self.pc.press_shortcut("win", "left")
        return "Workspace optimized for coding. Good luck, sir."

    async def set_presentation_mode(self):
        print("Friday: Setting up Presentation Mode.")
        self.smarthome.control_lights("bright")
        self.launcher.launch("PowerPoint")
        # Mute notifications
        # self.pc.toggle_do_not_disturb()
        return "Workspace ready for the presentation."

    async def execute_workflow(self, workflow_name):
        if workflow_name == "coding":
            return await self.set_coding_mode()
        elif workflow_name == "presentation":
            return await self.set_presentation_mode()
        return "Unknown workflow."
