import os
import shutil

class FileManager:
    def create_file(self, path, content=""):
        with open(path, "w") as f:
            f.write(content)

    def delete_file(self, path):
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)

    def list_files(self, directory="."):
        return os.listdir(directory)
