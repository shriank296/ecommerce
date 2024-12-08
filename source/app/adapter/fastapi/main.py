from fastapi import FastAPI

app = FastAPI(title="Ecommerce app")


@app.get('/')
def hello():
    return {"message": "hello ecommerce"}