from fastapi import FastAPI

from .routers import auth, contacts

app = FastAPI()
app.include_router(contacts.router)
app.include_router(auth.router, prefix='/api')

@app.get("/")
async def root():
    return {"message":"Hello Fast"}


