from fastapi import APIRouter, Cookie, Response
from typing import Optional
import back.services.chat_services as chat_serv
import back.services.dynamo_service as dynamo_serv
import back.services.classifier_service as classifier_service
import uuid
from back.schemas import ChatInput
from back.models.log_models import MessageLog


router = APIRouter(prefix="/chat")


@router.post("/message")
async def handle_message(message: str, response: Response, session_id: Optional[str] = Cookie(None)):
    if session_id is None:
        session_id = await chat_serv.create_session_id(response)

    

    dynamo_serv.log_message(MessageLog(session_id, message))

    text = ChatInput(session_id, message)
    intent = classifier_service.intent_classifier(text)

    #conversation = dynamo_serv.get_conversation(session_id)
    #escalate, reason = should_escalate(intent, conversation)