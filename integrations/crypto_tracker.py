import requests
import logging

class CryptoTracker:
    def get_price(self, coin="bitcoin"):
        try:
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
            response = requests.get(url, timeout=10).json()
            price = response.get(coin, {}).get("usd")
            if price:
                return f"The current price of {coin} is ${price}."
            return f"I couldn't fetch the price for {coin}. Please check the coin name."
        except Exception as e:
            logging.error(f"Crypto tracking failed: {e}")
            return "I encountered an error while fetching crypto prices."
