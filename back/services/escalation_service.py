from back.config import settings

async def should_escalate(intent_result, conversation):
    intent = intent_result.session_state.intent if intent_result.session_state else None
    if intent and intent.name == "escalation_request":
        return True, "customer asked for human"

    if intent_result.confidence_score is None or intent_result.confidence_score < settings.CONFIDENCE_THRESHOLD:
        return True, "low confidence score"

    # TODO: Add bot turn count

    return False, None