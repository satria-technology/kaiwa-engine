from fastapi import APIRouter, Request, HTTPException, Response
from pydantic import BaseModel
from twilio.twiml.messaging_response import MessagingResponse
import structlog

router = APIRouter()
log = structlog.get_logger()


class WhatsappWebhookPayload(BaseModel):
    MessageSid: str
    AccountSid: str
    From: str
    To: str
    Body: str


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

    resp = MessagingResponse()
    resp.message("Hello! Thank you for your message.")

    return Response(content=resp.to_xml(), media_type="application/xml")
