from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.settings import settings
from typing import Generator

# Criar engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Verifica conexões antes de usar
    echo=False  # True para debug SQL
)

# Criar session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency para obter sessão do banco
def get_db() -> Generator[Session, None, None]:
    """
    Cria uma sessão do banco de dados para cada request.
    Usa yield para garantir que a sessão seja fechada após o uso.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()