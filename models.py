from sqlalchemy import Column, String, BigInteger, Integer, func, TIMESTAMP
from db_base import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True)
    status = Column(String(250), nullable=False, default='active')
    created_at = Column(TIMESTAMP, nullable=False, default=func.current_timestamp())

    def __repr__(self):
        return f"<USER {self.user_id}"


