import requests

class CryptoTracker:
    def get_price(self, coin="bitcoin"):
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
        response = requests.get(url).json()
        price = response.get(coin, {}).get("usd")
        if price:
            return f"The current price of {coin} is ."
        return "I couldn't fetch the crypto price right now."
