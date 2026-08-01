from fastapi import FastAPI, APIRouter
from back.schemas import ChatResponse, ChatText
from back.config import settings

chat_router = APIRouter(prefix="/api/chat")

@chat_router.post("/", response_model=ChatResponse)
async def intent_classifier(text: ChatText, session_id):
    async with settings.session.client("lexv2-runtime", region_name=settings.AWS_REGION) as client:
        response = await client.recognize_text(
            botId = settings.BOT_ID,
            botAliasId = settings.BOT_ALIAS_ID,
            localeId = settings.LOCALE_ID,
            sessionId = session_id,
            text = text.text
        )

        interpretations = response.get("interpretations", [])
        top = interpretations[0] if interpretations else None

        return ChatResponse(
            messages=response.get("messages", []),
            session_state=response.get("sessionState", {}),
            session_id=response.get("sessionId", ""),
            confidence_score=top.get("nluConfidence", {})
        )