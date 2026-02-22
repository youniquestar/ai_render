from fastapi import APIRouter, HTTPException
from schemas import (
    ChatRequest, ChatResponse, 
    ReportRequest, ReportResponse,
    FollowUpNextRequest, FollowUpNextResponse,
    FollowUpRespondRequest, FollowUpRespondResponse
)

# To import the underlying NLP logic
from nlp.initial_triage import triage_chat
from nlp.follow_up import follow_up
from nlp.session import get_state

# This creates the router module
router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
def handle_chat(req: ChatRequest):
    """Handles the main triage conversation."""
    reply_text = triage_chat(req.user_id, req.message)
    return ChatResponse(reply=reply_text)

@router.post("/report", response_model=ReportResponse)
def handle_report(req: ReportRequest):
    """Generates the structured report for the C# database."""
    data = get_state(req.user_id).get("data", {})
    
    # To extract symptoms and triggers, ensuring they are lists
    symptoms_data = data.get('symptoms', ["None reported"])
    triggers_data = data.get('triggers', ["None identified"])
    
    symptoms_list = [symptoms_data] if isinstance(symptoms_data, str) else symptoms_data
    triggers_list = [triggers_data] if isinstance(triggers_data, str) else triggers_data

    # To build the summary text
    summary_text = (
        f"Patient assessment for {req.user_id}. "
        f"Duration: {data.get('duration', 'N/A')}. "
        f"Severity: {data.get('severity', 'N/A')}."
    )
    
    return ReportResponse(
        summary=summary_text,
        symptoms=symptoms_list,
        triggers=triggers_list
    )

@router.post("/followup/next", response_model=FollowUpNextResponse)
def handle_followup_next(req: FollowUpNextRequest):
    """Determines the next clarifying question."""
    # Placeholder: Replace with your logic to get the next question
    next_question = "Have you experienced any shortness of breath recently?"
    return FollowUpNextResponse(prompt=next_question)

@router.post("/followup/respond", response_model=FollowUpRespondResponse)
def handle_followup_respond(req: FollowUpRespondRequest):
    """Processes the patient's answer to the follow-up question."""
    reply_text = follow_up(req.user_id, req.message)
    return FollowUpRespondResponse(reply=reply_text)