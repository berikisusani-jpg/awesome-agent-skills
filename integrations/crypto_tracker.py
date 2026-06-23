import httpx
import logging
from integrations.base import BaseIntegration
import datetime

class CryptoTracker(BaseIntegration):
    @property
    def name(self): return "Finance"

    def available(self): return True

    async def execute(self, action, params=None):
        if action == "get_price":
             coin = (params or {}).get("coin", "bitcoin")
             return await self.get_price(coin)
        return {"status": "not_implemented"}

    async def get_price(self, coin="bitcoin"):
        try:
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
            async with httpx.AsyncClient() as client:
                response = (await client.get(url, timeout=10)).json()
            price = response.get(coin, {}).get("usd")
            if price:
                msg = f"The current price of {coin} is ${price}."
                return {
                    "status": "success",
                    "message": msg,
                    "receipt": {"type": "finance_receipt", "coin": coin, "price": price, "timestamp": datetime.datetime.now().isoformat()}
                }
            return {"status": "error", "message": f"I couldn't fetch the price for {coin}."}
        except Exception as e:
            logging.error(f"Crypto tracking failed: {e}")
            return {"status": "error", "message": str(e)}
