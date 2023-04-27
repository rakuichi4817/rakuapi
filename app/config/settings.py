"""バックエンドアプリの基本設定内容"""
from pydantic import BaseSettings


class Settings(BaseSettings):
    """APIサーバの設定項目"""

    TITLE = "Raku API"
    DESCRIPTION = "RakuichiのAPI"
    VERSION = "0.1.0"

    ORIGINS = ["http://localhost"]

    API_PREFIX = "/api/v1"


class MainDevSettings(Settings):
    """本番、開発環境の設定内容

    Notes
    -----
    インスタンス設定などを追加
    """

    pass
