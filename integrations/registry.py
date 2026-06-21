class UniversalRegistry:
    def __init__(self):
        self.categories = {
            "Core": ["Weather", "Calendar", "Gmail", "Spotify", "HomeAssistant"],
            "Social": ["Twitter", "LinkedIn", "Discord"],
            # ... others
        }

    def get_all_services(self):
        services = []
        for cat in self.categories.values():
            services.extend(cat)
        return services

    def get_service_count(self):
        return len(self.get_all_services())
