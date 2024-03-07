from fastapi import FastAPI
from app.api import roles, users, sup, rent
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Include routers
app.include_router(roles.router, prefix="/api", tags=["roles"])
app.include_router(users.router, prefix="/api", tags=["users"])
app.include_router(sup.router, prefix="/api", tags=["sups"])
app.include_router(rent.router, prefix="/api", tags=["rents"])


app.mount("/media", StaticFiles(directory="media"), name="media")
