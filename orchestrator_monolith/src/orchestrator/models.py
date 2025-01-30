from typing import List
from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str
    password: str


class UpdatePassword(BaseModel):
    old_password: str
    new_password: str


class UserIds(BaseModel):
    ids: List[int]

class SubscriptionRequest(BaseModel):
    email: str
    subscription_type: str

class ExtendSubscriptionRequest(BaseModel):
    email: str
    period: str  

class EmailList(BaseModel):
    emails: list[str]

class ActivateRequest(BaseModel):
    amount: int