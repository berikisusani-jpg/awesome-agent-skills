import os
import shutil
import logging
from config.settings import WORKSPACE_ROOT

class FileManager:
    def __init__(self):
        self.workspace_root = os.path.abspath(WORKSPACE_ROOT)
        if not os.path.exists(self.workspace_root):
            os.makedirs(self.workspace_root)

    def _safe_path(self, path):
        abs_path = os.path.abspath(os.path.join(self.workspace_root, path))
        # FIXED: Use commonpath to avoid sibling-directory bug
        if os.path.commonpath([abs_path, self.workspace_root]) != self.workspace_root:
            raise PermissionError(f"Access denied: {path} is outside the workspace root.")
        return abs_path

    def create_file(self, path, content="", confirm=False):
        if not confirm:
            return "Error: Explicit confirmation required to create files."
        target = self._safe_path(path)
        with open(target, "w") as f:
            f.write(content)
        return f"File created at {path}"

    def delete_file(self, path, confirm=False):
        if not confirm:
            return "Error: Explicit confirmation required for destructive actions."

        target = self._safe_path(path)
        if os.path.isfile(target):
            os.remove(target)
            return f"File {path} deleted."
        elif os.path.isdir(target):
            shutil.rmtree(target)
            return f"Directory {path} deleted."
        return f"Path {path} not found."

    def list_files(self, directory="."):
        target = self._safe_path(directory)
        return os.listdir(target)
