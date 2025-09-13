from fastapi import FastAPI, Depends
from app.routes import user_routes as usercrud
from app.routes import task_routes as taskcrud
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine,Base
Base.metadata.create_all(bind=engine)
app = FastAPI(title="Prodexa API")

origins={
    'http://localhost:3000/',
     "http://127.0.0.1:3000",
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],         # frontend origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],           # allow all HTTP methods (GET, POST, PUT, DELETE, OPTIONS)
    allow_headers=["*"],  
)

app.include_router(usercrud.router)
app.include_router(taskcrud.router)


