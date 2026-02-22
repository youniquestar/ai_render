from pydantic import BaseModel
from typing import List

class ChatRequest(BaseModel):
    user_id: str
    message: str

class ReportRequest(BaseModel):
    user_id: str

class FollowUpNextRequest(BaseModel):
    user_id: str

class FollowUpRespondRequest(BaseModel):
    user_id: str
    message: str

class ChatResponse(BaseModel):
    reply: str

class ReportResponse(BaseModel):
    summary: str
    symptoms: List[str]
    triggers: List[str]

class FollowUpNextResponse(BaseModel):
    prompt: str

class FollowUpRespondResponse(BaseModel):
    reply: str