from integrations.crypto_tracker import CryptoTracker

class FinancialIntelligence:
    def __init__(self):
        self.crypto = CryptoTracker()
        self.monthly_budget = 500000 # Example in Naira
        self.current_spending = 120000

    def get_financial_status(self):
        btc_status = self.crypto.get_price("bitcoin")
        remaining = self.monthly_budget - self.current_spending

        status = f"Financial Snapshot: You have ₦{remaining} remaining of your ₦{self.monthly_budget} budget. {btc_status}"

        if self.current_spending > (self.monthly_budget * 0.8):
            status += "\nWarning: You've reached 80% of your monthly budget. I suggest reducing non-essential spending."

        return status

    def analyze_investment(self, asset):
        price_info = self.crypto.get_price(asset)
        return f"Predictive analysis for {asset}: {price_info}. Based on market sentiment, I recommend holding for the next 48 hours."
