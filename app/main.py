from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import json
import os

app = FastAPI(title="WAHA WhatsApp API")

# Carrega variáveis de ambiente
WAHA_URL = os.getenv("WAHA_URL", "http://localhost:3000")

# Carrega os contatos
with open("data/contacts.json", "r") as f:
    CONTACTS = json.load(f)

# Tool: send_message
class MessageRequest(BaseModel):
    number: str
    message: str

@app.post("/tool/send_message")
async def send_message(req: MessageRequest):
    """
    Envia mensagem via WhatsApp usando WAHA.
    O número deve estar no formato internacional (+55...)
    """
    try:
        # Remove o + do número se existir
        number = req.number.replace("+", "")
        
        response = requests.post(
            f"{WAHA_URL}/api/sendText",
            headers={"Content-Type": "application/json"},
            json={
                "chatId": f"{number}@c.us",
                "text": req.message,
                "session": "default"
            }
        )
        
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
            
        return response.json()
        
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

# Resource: contatos
@app.get("/resource/contatos")
def get_contacts():
    """Retorna lista de contatos pré-configurados"""
    return CONTACTS 