import httpx
from app.core.config import get_settings

settings = get_settings()

class WhatsAppService:
    async def send_message(self, number: str, message: str) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.WAHA_URL}/api/sendText",
                json={
                    "chatId": f"{number}@c.us",
                    "text": message,
                    "session": "default"
                }
            )
            return response.json() 