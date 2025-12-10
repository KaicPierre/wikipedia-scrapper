from fastapi import APIRouter, HTTPException, Depends

from app.schemas.summary import CreateSummaryRequest
from sqlalchemy.orm import Session
from app.database.connection import get_db

from app.services.scrapper import Scrapper
from app.services.summarizer import Summarizer
from app.repositories.summary import SummaryRepository


router = APIRouter(prefix='/summary', tags=['Summary'])

@router.get('/{page_name}')
def get_summary_by_url(page_name: str, db: Session = Depends(get_db)):
    try:
        url = Scrapper().create_url(page_name)
        repo = SummaryRepository(db)
        existing = repo.get_by_url(url)
        if existing:
            return {"summary": existing.summary_data}
        else:
            raise ValueError("There is no Summary for this URL")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/')
def summarize(data: CreateSummaryRequest, db: Session = Depends(get_db)):
    try:
        repo = SummaryRepository(db)
        existing = repo.get_by_url(data.url)
        
        if existing:
            return {"summary": existing.summary_data}
    
        page = Scrapper().scrap_page(data.url)
        summary = Summarizer().summarize(data=page, word_count=data.word_count)
        new_summary = repo.create(data.url, summary)

        return {"message": new_summary.summary_data}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
