import os
import subprocess
import sys

def install_deps():
    print("Installing Project FRIDAY dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("Dependencies installed successfully.")

def init_env():
    if not os.path.exists(".env"):
        shutil.copy(".env.example", ".env")
        print(".env file created.")

def main():
    print("--- Project FRIDAY Setup ---")
    install_deps()
    print("Setup finished. Run 'python main.py' to start Friday.")

if __name__ == "__main__":
    import shutil
    main()
