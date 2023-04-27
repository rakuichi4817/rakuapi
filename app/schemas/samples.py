"""/v1/samplesのpydanticスキーマ"""
from fastapi import Query
from pydantic import BaseModel, Field


class AddIn(BaseModel):
    """GET /plus の入力"""

    a: int | float = Field(Query(description="足される数"))
    b: int | float = Field(Query(description="足される数"))


class AddOut(BaseModel):
    """GET /plus の出力"""

    result: int | float = Field(description="足し算の結果")
