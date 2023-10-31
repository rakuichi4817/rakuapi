# ----------ベースイメージの指定----------
FROM python:3.11-slim AS base

ARG workdir="/rakuapi"
WORKDIR $workdir

RUN apt-get update && pip install --upgrade pip 

# ----------開発用(.devcontainerが接続する用----------
FROM base AS devcontainer
# devcontainer上では仮想環境を作って開発する
RUN apt-get install -y git \
    && pip install pipenv

# ----------本番環境用ビルダー----------
FROM base as builder
RUN pip install pipenv 

# ライブラリをシステムへ直接書き込む
COPY Pipfile Pipfile.lock $workdir/
RUN pipenv sync --system 

# ----------ドキュメントビルダー----------
FROM base as mkdocs-builder
# mkdocs用ライブラリを入れる
RUN pip install mkdocs mkdocs-material mkdocs-render-swagger-plugin mkdocs-awesome-pages-plugin
WORKDIR /build
COPY ./docs /build/docs
COPY mkdocs.yml /build/
RUN mkdocs build

# ----------本番APP用----------
FROM base AS app

# ビルダーで展開したライブラリをアプリ用コンテナにコピー
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages/
COPY --from=builder /usr/local/bin/uvicorn /usr/local/bin/uvicorn
COPY --from=mkdocs-builder ./build/site /rakuapi/site
COPY ./app $workdir/app

EXPOSE 8000
HEALTHCHECK CMD curl --fail <http://localhost:8000/_stcore/health>
ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

