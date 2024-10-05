import datetime
from fastapi import APIRouter, Request, HTTPException, Response
from pydantic import BaseModel
from twilio.twiml.messaging_response import MessagingResponse
from application.conversation import conversation_service
from domain.conversation.model import Message, Participant
import structlog

from interfaces.fastapi.twilio_dto import WhatsappWebhookPayload, parse_request_to_whatsapp_webhook_payload

router = APIRouter()
log = structlog.get_logger()

# https://www.twilio.com/docs/messaging/guides/webhook-request
@router.post("/whatsapp-webhook")
async def handle_whatsapp_webhook(request: Request):
    form = await request.form()
    try:
        payload = WhatsappWebhookPayload(
            MessageSid=form["MessageSid"],
            AccountSid=form["AccountSid"],
            From=form["From"],
            To=form["To"],
            Body=form["Body"],
        )
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing required field: {e}")

    log.info("Received WhatsApp message", body=payload.Body)

    response_message = conversation_service.respond_to_message(payload.to_message())

    resp = MessagingResponse()
    resp.message(response_message.message)

    return Response(content=resp.to_xml(), media_type="application/xml")
