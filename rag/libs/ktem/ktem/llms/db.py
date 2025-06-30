import uuid
from datetime import datetime
from typing import Type

from ktem.db.engine import engine
from sqlalchemy import JSON, Boolean, Column, String, UUID, DateTime
from sqlalchemy.orm import DeclarativeBase
from theflow.settings import settings as flowsettings
from theflow.utils.modules import import_dotted_string
from tzlocal import get_localzone


class Base(DeclarativeBase):
    pass


class BaseLLMTable(Base):
    """Base table to store language model"""

    __abstract__ = True

    name = Column(String, primary_key=True, unique=True)
    spec = Column(JSON, default={})
    default = Column(Boolean, default=False)


class DocumentLMBaseLLMTable(Base):
    """Base table to store language model"""

    __abstract__ = True

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, primary_key=True, unique=True)
    spec = Column(JSON, default={})
    default = Column(Boolean, default=False)
    created_at = Column(
        DateTime(timezone=True), default=datetime.now(get_localzone())
    )
    updated_at = Column(
        DateTime(timezone=True), default=datetime.now(get_localzone())
    )


_base_llm: Type[DocumentLMBaseLLMTable] = (
    import_dotted_string(flowsettings.KH_TABLE_LLM, safe=False)
    if hasattr(flowsettings, "KH_TABLE_LLM")
    else DocumentLMBaseLLMTable
)


class LLMTable(_base_llm):  # type: ignore
    __tablename__ = "system_llm"


if not getattr(flowsettings, "KH_ENABLE_ALEMBIC", False):
    LLMTable.metadata.create_all(engine)
