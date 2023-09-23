from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config import Config

Base = declarative_base()


class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=True)
    email = Column(String, nullable=True)


connect_args = {}
kwargs = {}

if Config.DB_ENGINE in ["sqlite-memory", "sqlite-file"]:
    connect_args = {"check_same_thread": False}

engine = create_engine(
    Config.DB_URL,
    connect_args=connect_args,
    **kwargs,
    echo=True
)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def get_database_session():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
