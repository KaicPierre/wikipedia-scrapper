from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.summary import Summary


class SummaryRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_url(self, url: str) -> Optional[Summary]:
        return self.db.query(Summary).filter(Summary.url == url).first()
    
    def create(self, url: str, summary_text: str) -> Summary:
        db_summary = Summary(
            url=url,
            summary_data=summary_text,
        )
        
        try:
            self.db.add(db_summary)
            self.db.commit()
            self.db.refresh(db_summary)
            return db_summary
        except IntegrityError:
            self.db.rollback()
            raise ValueError(f"Summary for URL '{url}' already exists")
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Summary]:
        return self.db.query(Summary).offset(skip).limit(limit).all()