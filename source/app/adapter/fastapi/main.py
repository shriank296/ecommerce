from fastapi import FastAPI
from source.app.adapter.fastapi.routes.api import api_router

app = FastAPI(title="Ecommerce app")


app.include_router(api_router)


@app.get('/')
def hello():
    return {"message": "hello ecommerce"}
