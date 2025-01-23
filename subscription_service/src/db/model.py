from sqlalchemy.orm import declarative_base
import sqlalchemy as sa

Base = declarative_base()

class Subscription(Base):
    __tablename__ = 'subscriptions'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    user_id = sa.Column(sa.Integer)
    email = sa.Column(sa.String, nullable=False, unique=True)
    subscription_type = sa.Column(sa.String, nullable=False)
    is_active = sa.Column(sa.Boolean, default=False)
    end_date = sa.Column(sa.Date, nullable=True)
