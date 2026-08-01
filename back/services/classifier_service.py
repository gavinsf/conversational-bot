from fastapi import FastAPI, APIRouter
from back.schemas import ChatResponse, ChatInput
from back.config import settings

async def intent_classifier(message: ChatInput):
    session_id = str(session_id)
    
    async with settings.session.client("lexv2-runtime", region_name=settings.AWS_REGION) as client:
        response = await client.recognize_text(
            botId = settings.BOT_ID,
            botAliasId = settings.BOT_ALIAS_ID,
            localeId = settings.LOCALE_ID,
            sessionId = session_id,
            text = message.text
        )

        interpretations = response.get("interpretations", [])
        top = interpretations[0] if interpretations else None

        return ChatResponse(
            messages=response.get("messages", []),
            session_state=response.get("sessionState", {}),
            session_id=session_id,   
            confidence_score=top.get("nluConfidence", {}).get("score") if top else None
        )