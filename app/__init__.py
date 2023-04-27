from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.v1 import api_router
from app.config.settings import MainDevSettings


def get_application(test: bool = False) -> FastAPI:
    """環境に合わせてアプリを作成する

    Parameters
    ----------
    test : bool, optional
        テスト環境の場合はTrue, by default False

    Returns
    -------
    FastAPI
        APIサーバ
    """
    # 環境毎に設定値の読み込み
    if test:
        raise ValueError("まだテストモードに対応していません")
    else:
        settings = MainDevSettings()
    app = FastAPI(title=settings.TITLE, description=settings.DESCRIPTION, version=settings.VERSION)

    # CORS設定
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # routerの設定
    app.include_router(api_router, prefix=settings.API_PREFIX)

    return app
