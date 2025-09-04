from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.api.v1.router import app as v1_router

app = FastAPI(
    title="AI Review Agent API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Auto redirect root "/" to "/docs"
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

# Include API routers
app.include_router(v1_router, prefix="/api/v1")
