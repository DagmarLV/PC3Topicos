from fastapi import FastAPI
from .database import Base, engine
from .routes import auth, accounts, transactions, logs
from .scripts import init_db

Base.metadata.create_all(bind=engine)

init_db()

app = FastAPI()

app.include_router(auth.router)
app.include_router(accounts.router)
app.include_router(transactions.router)
app.include_router(logs.router)