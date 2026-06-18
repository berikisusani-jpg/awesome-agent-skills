import os
import psutil
import platform

class AutoOnboarding:
    def __init__(self):
        self.system_info = {
            "platform": platform.system(),
            "version": platform.version(),
            "processor": platform.processor()
        }

    def scan_environment(self):
        print("Scanning environment for onboarding...")
        detected_apps = []
        # Check for common apps
        apps_to_check = ["chrome", "vscode", "spotify", "slack", "discord"]
        for process in psutil.process_iter(['name']):
            try:
                name = process.info['name'].lower()
                for app in apps_to_check:
                    if app in name and app not in detected_apps:
                        detected_apps.append(app)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return detected_apps

    def get_welcome_message(self, user_name="User"):
        apps = self.scan_environment()
        apps_str = ", ".join(apps) if apps else "nothing specific yet"
        return f"Welcome back, {user_name}. I've detected {apps_str} running on your system. I'm ready to take control whenever you need."
