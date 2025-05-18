from typing import List, Dict
import openai
from .config import get_settings

settings = get_settings()

class WhatsAppAGI:
    def __init__(self):
        self.context = {
            "role": "system",
            "content": """Você é um assistente especializado em atendimento via WhatsApp.
            Você deve ser cordial, profissional e objetivo em suas respostas."""
        }
        
    async def process_message(self, message: str, history: List[Dict] = None) -> str:
        messages = [self.context]
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": message})
        
        response = openai.ChatCompletion.create(
            model=settings.MODEL_NAME,
            messages=messages
        )
        
        return response.choices[0].message.content 