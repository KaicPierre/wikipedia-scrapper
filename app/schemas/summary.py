from pydantic import BaseModel

class SummaryResponse(BaseModel):
  id: int
  url: str
  summary: str
  created_at: str
  updated_at: str
  
class CreateSummaryRequest(BaseModel):
  url: str
  word_count: int