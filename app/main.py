from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # ← AGREGAR
from .database import Base, engine
from .routes import auth, accounts, transactions, logs
from .scripts import init_db

Base.metadata.create_all(bind=engine)
init_db()

app = FastAPI()

# ← AGREGAR ESTAS LÍNEAS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# El resto igual
app.include_router(auth.router)
app.include_router(accounts.router)
app.include_router(transactions.router)
app.include_router(logs.router)