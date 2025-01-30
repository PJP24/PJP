from sqlalchemy.orm import declarative_base
import sqlalchemy as sa

Base = declarative_base()

class Subscription(Base):
    __tablename__ = 'subscriptions'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    user_id = sa.Column(sa.Integer)
    is_active = sa.Column(sa.Boolean, default=False)
    end_date = sa.Column(sa.Date, nullable=True)
    subscription_type = sa.Column(sa.String, nullable=True)
