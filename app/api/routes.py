from fastapi import APIRouter, HTTPException
from .models import MessageRequest, MessageResponse
from app.services.whatsapp import WhatsAppService
from app.core.agi import WhatsAppAGI
from typing import Annotated

router = APIRouter()
whatsapp_service = WhatsAppService()
agi = WhatsAppAGI()

@router.post("/send_message", response_model=MessageResponse)
async def send_message(request: Annotated[MessageRequest, MessageRequest]):
    try:
        # Processa a mensagem com a AGI
        processed_message = await agi.process_message(request.message)
        
        # Envia a mensagem processada
        result = await whatsapp_service.send_message(
            request.number, 
            processed_message
        )
        
        return MessageResponse(
            success=True,
            message_id=result.get("id")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 