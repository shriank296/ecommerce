from fastapi import FastAPI
from source.app.adapter.db.model import Base, Cart, CartItem, Category, Order, OrderItem, Product, User

app = FastAPI(title="Ecommerce app")

@app.on_event("startup")
# async def startup_event():
#     print("Creating tables...")
#     print(Base.metadata.tables)
#     Base.metadata.drop_all(engine)
#     Base.metadata.create_all(engine)
#     print("Tables created.")




@app.get('/')
def hello():
    return {"message": "hello ecommerce"}