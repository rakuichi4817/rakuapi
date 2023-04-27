"""エンドポイントの設定

routers内に作成したエンドポイントを指定
"""
from fastapi import APIRouter

from app.v1.routers import samples, images, dataanalysis


# 各種モジュールの設定
api_router = APIRouter()
api_router.include_router(samples.router, tags=["サンプル"], prefix="/sample")
api_router.include_router(images.router, tags=["画像処理"], prefix="/images")
api_router.include_router(dataanalysis.router, tags=["データ処理"], prefix="/dataanalysis")
