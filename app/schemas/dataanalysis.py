"""/v1/routers/dataanalysisのpydanticスキーマ"""
from fastapi import Body
from pydantic import BaseModel


class GenereteColumnInfo(BaseModel):
    """GET /dataanalysis/generate-table の１つの項目情報"""

    column_name: str = Body(description="項目名", default="項目〇")
    column_type: str = Body(description="int or float", default="int")
    min_val: int | float = Body(description="最小値")
    max_val: int | float = Body(description="最大値")


class GenerateTableIn(BaseModel):
    columns: list[GenereteColumnInfo]
    record_cnt: int = Body(description="生成レコード数")
