from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base


Base = declarative_base()

class Subscription(Base):
    __tablename__ = 'subscriptions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False, unique=True)
    subscription_type = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
