from fastapi import APIRouter, File
from starlette.responses import Response

from app.libs.images import face_mosaic


router = APIRouter()


@router.post("/mosaic")
def mosaic(file: bytes = File(..., description="モザイクをつける画像")):
    """# 顔にモザイクを追加する

    ## Parameters

    - file_byte(bytes): 画像データ
    """
    mosaic_byte = face_mosaic(file)
    return Response(mosaic_byte, media_type="image/png")
