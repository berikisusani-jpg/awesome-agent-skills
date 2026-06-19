class UniversalRegistry:
    def __init__(self):
        self.integrations = {
            "Social": ["Twitter", "LinkedIn", "Discord", "Slack", "Reddit", "Facebook", "Instagram", "Mastodon", "Telegram", "WhatsApp"],
            "Dev": ["GitHub", "GitLab", "Bitbucket", "Jira", "Trello", "Heroku", "Netlify", "Vercel", "DigitalOcean", "Linode", "DockerHub", "Firebase", "AWS", "Azure", "GCP", "Postman", "Sentry", "NewRelic", "CircleCI", "TravisCI"],
            "Finance": ["Stripe", "PayPal", "Coinbase", "Binance", "Plaid", "Robinhood", "Wise", "Revolut", "Venmo", "CashApp"],
            "Productivity": ["Notion", "Evernote", "Todoist", "GoogleDrive", "Dropbox", "Slack", "MicrosoftTeams", "Zoom", "Calendly", "Asana", "Monday", "ClickUp", "AirTable", "Zapier", "IFTTT", "Grammarly", "Otter", "Loom", "Miro", "Figma"],
            "IoT": ["HomeAssistant", "PhilipsHue", "Nest", "Ring", "Ecobee", "Sonos", "TP-Link", "Wyze", "Arlo", "SimpliSafe"],
            "Entertainment": ["Spotify", "AppleMusic", "YouTube", "Netflix", "DisneyPlus", "Twitch", "Steam", "EpicGames", "Audible", "PocketCasts"],
            "Marketing": ["Mailchimp", "HubSpot", "Salesforce", "Intercom", "Buffer", "Hootsuite", "ConstantContact", "SendGrid", "Twilio", "ActiveCampaign"],
            "Cloud_Services": ["Cloudflare", "Akamai", "Fastly", "Auth0", "Okta", "Supabase", "PlanetScale", "Hasura", "Upstash", "RedisCloud"]
        }

    def get_all_services(self):
        all_services = []
        for category in self.integrations.values():
            all_services.extend(category)
        return all_services

    def get_service_count(self):
        return len(self.get_all_services())

    def get_connection_stub(self, service_name):
        return f"Connecting to {service_name}... Authentication required."
