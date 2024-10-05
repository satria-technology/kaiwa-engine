from fastapi import APIRouter, Request, HTTPException, Response
from twilio.twiml.messaging_response import MessagingResponse
from application.conversation import conversation_service
import structlog

from interfaces.fastapi.twilio_dto import WhatsappWebhookPayload

router = APIRouter(
    prefix="/twilio",
)
log = structlog.get_logger()

# https://www.twilio.com/docs/messaging/guides/webhook-request
@router.post("/whatsapp-webhook")
async def handle_whatsapp_webhook(request: Request):
    try:
        form = await request.form()
        log.debug("Received form", form=form)
        payload = WhatsappWebhookPayload(**form)
    except KeyError as e:
        log.error("Missing required field", error=str(e), exc_info=True)
        raise HTTPException(status_code=422, detail=f"Missing required field: {e}")
    except ValueError as e:
        log.error("Invalid value", error=str(e), exc_info=True)
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        log.error("Unknown error", error=str(e), exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))

    log.info("Received WhatsApp message", body=payload.Body)

    try:
        response_message = conversation_service.respond_to_message(payload.to_message())
    except Exception as e:
        log.error("Error processing message", error=str(e))
        raise HTTPException(status_code=500, detail="Error processing message")

    resp = MessagingResponse()
    resp.message(response_message.message)

    return Response(content=resp.to_xml(), media_type="application/xml")
