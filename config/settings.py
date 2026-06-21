import os
from dotenv import load_dotenv

load_dotenv()

def get_env_var(name, default=None, required=False):
    val = os.getenv(name, default)
    if required and not val:
        # For required vars, we might want to log or raise if not in dev
        pass
    return val

ANTHROPIC_API_KEY = get_env_var("ANTHROPIC_API_KEY")
OPENAI_API_KEY = get_env_var("OPENAI_API_KEY")
SUPABASE_URL = get_env_var("SUPABASE_URL")
SUPABASE_KEY = get_env_var("SUPABASE_KEY")
ELEVENLABS_API_KEY = get_env_var("ELEVENLABS_API_KEY")
PICOVOICE_ACCESS_KEY = get_env_var("PICOVOICE_ACCESS_KEY")
GEMINI_API_KEY = get_env_var("GEMINI_API_KEY")

# Friday Security
FRIDAY_API_TOKEN = get_env_var("FRIDAY_API_TOKEN")

# New integrations
OPENWEATHERMAP_API_KEY = get_env_var("OPENWEATHERMAP_API_KEY")
SPOTIFY_CLIENT_ID = get_env_var("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = get_env_var("SPOTIFY_CLIENT_SECRET")
HOME_ASSISTANT_TOKEN = get_env_var("HOME_ASSISTANT_TOKEN")

# Other settings
LOG_FILE = "friday.log"

# Sandbox Security
WORKSPACE_ROOT = os.path.join(os.getcwd(), "friday_workspace")
if not os.path.exists(WORKSPACE_ROOT):
    os.makedirs(WORKSPACE_ROOT)

# Power Levels (Autonomy Profiles)
# GUEST: Everything requires approval.
# STANDARD: Read-only auto-approves, destructive requires approval.
# POWER: PC/Browser auto-approves, file deletion requires approval.
AUTONOMY_PROFILE = get_env_var("AUTONOMY_PROFILE", "GUEST")
