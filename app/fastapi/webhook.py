from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel

router = APIRouter()


class WebhookPayload(BaseModel):
    event: str
    data: dict


@router.post("/webhook")
async def handle_webhook(payload: WebhookPayload):
    # Process the webhook payload
    if payload.event == "example_event":
        # Handle the specific event
        return {"status": "success", "message": "Webhook received and processed"}
    else:
        raise HTTPException(status_code=400, detail="Unsupported event type")
