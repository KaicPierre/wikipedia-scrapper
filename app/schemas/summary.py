from pydantic import BaseModel, Field

class SummaryResponse(BaseModel):
  id: int
  url: str
  summary: str
  created_at: str
  updated_at: str
  
class CreateSummaryRequest(BaseModel):
    """Requisição para criar um novo resumo de artigo da Wikipedia."""
    url: str = Field(
        ...,
        description="URL completa do artigo da Wikipedia em português",
        pattern=r"^https://pt\.wikipedia\.org/wiki/.+$",
        example="https://pt.wikipedia.org/wiki/Python_(linguagem_de_programação)"
    )
    word_count: int = Field(
        ...,
        description="Número aproximado de palavras desejadas no resumo",
        ge=10,
        le=500,
        example=100
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://pt.wikipedia.org/wiki/Python_(linguagem_de_programação)",
                "word_count": 100
            }
        }

class SummaryResponseData(BaseModel):
    """Resposta simplificada contendo apenas o resumo."""
    summary: str = Field(
        ...,
        description="Texto do resumo gerado ou recuperado",
        example="Python é uma linguagem de programação de alto nível..."
    )
