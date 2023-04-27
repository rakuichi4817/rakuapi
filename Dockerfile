# -----ベースイメージの指定-----
FROM python:3.10-slim AS base

ARG workdir="/workspace"
WORKDIR $workdir
RUN ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime

RUN apt-get update && pip install --upgrade pip \
    && apt-get install -y libopencv-dev

# -----本番環境用ビルダー-----
FROM base as builder
RUN pip install pipenv 

# ライブラリをシステムへ直接書き込む
COPY Pipfile Pipfile.lock $workdir/
RUN pipenv sync --system
EXPOSE 8000

# -----本番APP用------
FROM base AS app

HEALTHCHECK CMD curl --fail <http://localhost:8000/_stcore/health>

# ビルダーで展開したライブラリをアプリ用コンテナにコピー
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages/
COPY --from=builder /usr/local/bin/uvicorn /usr/local/bin/uvicorn
COPY . $workdir

ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# -----開発用(.devcontainerが接続する用)-----
FROM base AS development
# devcontainer上では仮想環境を作って開発する
RUN apt-get install -y git \
    && pip install pipenv