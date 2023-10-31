import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

site_dir = "site"
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


if os.path.exists(site_dir):
    # サイトページが存在していたらマウントする
    app.mount("/devdocs", StaticFiles(directory=site_dir, html=True), name="site")
