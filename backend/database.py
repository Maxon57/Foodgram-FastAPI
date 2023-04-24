from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings import settings
from redis import Redis


engine = create_engine(
    settings.database_url,
    connect_args={'check_same_thread': False}
)

redis_conn = Redis(host='localhost', port=6379, db=0, decode_responses=True)

Session = sessionmaker(
    engine,
    autocommit=False,
    autoflush=False
)


def get_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()
