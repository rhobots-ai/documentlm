from typing import Optional

from ktem.db.engine import engine
from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel
from theflow.settings import settings


# TODO: simplify with using SQLAlchemy directly
class OldIndex(SQLModel):
    __table_args__ = {"extend_existing": True}
    __tablename__ = "ktem__index"  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    index_type: str = Field()
    config: dict = Field(default={}, sa_column=Column(JSON))


class Index(SQLModel, table=True):
    """Base table to store language model"""

    __tablename__ = "system_index"

    id: int = Field(primary_key=True, index=True)
    name: str = Field(unique=True)
    index_type: str = Field()
    config: dict = Field(default=[], sa_column=Column(JSON))


if not getattr(settings, "KH_ENABLE_ALEMBIC", False):
    Index.metadata.create_all(engine)
