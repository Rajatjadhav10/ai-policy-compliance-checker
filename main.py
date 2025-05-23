from fastapi import FastAPI
from routers import upload, ask

app = FastAPI(title="AI Policy Compliance API")

# Mount the /upload/pdf route from upload.py
app.include_router(upload.router, prefix="/upload")
app.include_router(ask.router, prefix="/ask")
# Health check or root route
@app.get("/")
def read_root():
    return {"message": "Welcome to the AI-Powered Policy Compliance Checker"}
