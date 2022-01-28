from typing import Optional

from pydantic import BaseModel, EmailStr


class SubscriptionEmailBase(BaseModel):
    email: Optional[EmailStr] = None


class SubscriptionEmailCreate(SubscriptionEmailBase):
    email: EmailStr


class SubscriptionEmailInDB(SubscriptionEmailBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class SubscriptionEmail(SubscriptionEmailInDB):
    pass
