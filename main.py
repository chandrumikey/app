from fastapi import FastAPI, Depends
from app.routes import user_routes as usercrud
from app.routes import task_routes as taskcrud

app = FastAPI(title="Prodexa API")

 
app.include_router(usercrud.router)
app.include_router(taskcrud.router)



