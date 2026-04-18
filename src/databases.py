import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from template.shared.infrastructure.persistence.base import Base  # noqa: F401

DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(DATABASE_URL, pool_size=0, pool_recycle=60, pool_pre_ping=False)


class SessionFactory:
    @staticmethod
    def create() -> Session:
        session: Session = sessionmaker(autocommit=False, autoflush=True, bind=engine)()
        return session
