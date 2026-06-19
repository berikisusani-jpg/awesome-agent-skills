import os
from dotenv import load_dotenv

load_dotenv()

def get_env_var(name, default=None, required=False):
    val = os.getenv(name, default)
    if required and not val:
        # We don't raise here to prevent crash on import, but we can log a warning
        # or handle it in the module that uses it.
        pass
    return val

ANTHROPIC_API_KEY = get_env_var("ANTHROPIC_API_KEY")
OPENAI_API_KEY = get_env_var("OPENAI_API_KEY")
SUPABASE_URL = get_env_var("SUPABASE_URL")
SUPABASE_KEY = get_env_var("SUPABASE_KEY")
ELEVENLABS_API_KEY = get_env_var("ELEVENLABS_API_KEY")
PICOVOICE_ACCESS_KEY = get_env_var("PICOVOICE_ACCESS_KEY")
GEMINI_API_KEY = get_env_var("GEMINI_API_KEY")

# New integrations
OPENWEATHERMAP_API_KEY = get_env_var("OPENWEATHERMAP_API_KEY")
SPOTIFY_CLIENT_ID = get_env_var("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = get_env_var("SPOTIFY_CLIENT_SECRET")
HOME_ASSISTANT_TOKEN = get_env_var("HOME_ASSISTANT_TOKEN")

# Other settings
LOG_FILE = "friday.log"
EOF_WORKSPACE_ROOT = os.getcwd() # For Part 4 allow-listing
