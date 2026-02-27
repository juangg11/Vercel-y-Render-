from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict
from sqlalchemy import create_engine, Integer, String, select
from sqlalchemy.orm import declarative_base, sessionmaker, Mapped, mapped_column, Session
from typing import Generator, Literal
import os
import time
import logging
from jose import JWTError, jwt
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

SECRET_KEY = os.getenv("JWT_SECRET", "ci_cd_secret_key_999")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI(title="API CI/CD", version="2.0.0")

Base = declarative_base()

class Item(Base):
    __tablename__ = "items"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)

class ItemCreate(BaseModel):
    name: str
    status: Literal["Pendiente", "En progreso", "Completado"]

class ItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    status: str

def build_database_url() -> str:
    db_url = os.getenv("DATABASE_URL")
    if db_url and db_url.startswith("mysql://"):
        return db_url.replace("mysql://", "mysql+pymysql://", 1)
    return db_url if db_url else "mysql+pymysql://root:pass@localhost/db"

engine = create_engine(build_database_url(), pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    exc = HTTPException(status_code=401, detail="Invalid token", headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = payload.get("sub")
        if user is None: raise exc
        return user
    except JWTError: raise exc

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username == "admin" and form_data.password == "12345":
        return {"access_token": create_access_token({"sub": form_data.username}), "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Incorrect credentials")

@app.get("/")
async def root():
    return {"status": "online", "docs": "/docs"}

@app.get("/api/items", response_model=list[ItemOut])
async def list_items(db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    return db.execute(select(Item)).scalars().all()

@app.post("/api/items", response_model=ItemOut)
async def create_item(payload: ItemCreate, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    item = Item(name=payload.name, status=payload.status)
    db.add(item)
    db.commit()
    db.refresh(item)
    logger.info(f"Item created by {user}")
    return item

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.on_event("startup")
def on_startup():
    for _ in range(5):
        try:
            Base.metadata.create_all(bind=engine)
            break
        except: time.sleep(5)