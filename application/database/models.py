from sqlalchemy import Column, Integer, String

from .base_class import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, index=True)

    email = Column(String, unique=True, index=True, nullable=False)

    hashed_password = Column(String, nullable=False)


class SubscriptionEmail(Base):
    __tablename__ = 'subscription_email'

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String, unique=True, index=True, nullable=False)
