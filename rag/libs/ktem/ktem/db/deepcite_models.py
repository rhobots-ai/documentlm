import uuid
from typing import Optional

from sqlalchemy import Column, JSON
from sqlmodel import SQLModel, Field


class BaseUser(SQLModel):
    """Store the user information

    Attributes:
        id: canonical id to identify the user
        email: the email of the user
    """

    __tablename__ = 'accounts_user'
    __table_args__ = {"extend_existing": True}

    id: str = Field(
        default_factory=lambda: uuid.uuid4().hex, primary_key=True, index=True
    )
    email: str = Field(unique=True)


class BaseSetting(SQLModel):
    """Record of user settings

    Attributes:
        id: canonical id to identify the settings
        user_id: the user id
        setting: the user settings (in dict/json format)
    """

    __tablename__ = 'accounts_setting'
    __table_args__ = {"extend_existing": True}

    id: str = Field(
        default_factory=lambda: uuid.uuid4().hex, primary_key=True, index=True
    )
    user_id: str = Field(default="")
    setting: dict = Field(default={}, sa_column=Column(JSON))


class BaseIssueReport(SQLModel):
    """Store user-reported issues

    Attributes:
        id: canonical id to identify the issue report
        issues: the issues reported by the user, formatted as a dict
        chat: the conversation id when the user reported the issue
        settings: the user settings at the time of the issue report
        user: the user id
    """

    __tablename__ = 'core_issuereport'
    __table_args__ = {"extend_existing": True}

    id: str = Field(default=None, primary_key=True)
    issues: dict = Field(default={}, sa_column=Column(JSON))
    chat: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    settings: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    user_id: Optional[str] = Field(default=None)
