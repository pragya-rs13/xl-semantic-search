from fastapi import FastAPI
from routes.healthcheck import router as health_router
from routes.search import router as search_router
from logger import logger
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Semantic Search Backend", version="0.1.0")

origins = [
    "http://localhost:8000",  # running a dev server
    "http://127.0.0.1:8000",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "null",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include routers
app.include_router(health_router, prefix="/api/v1")
app.include_router(search_router, prefix="/api/v1")


# set up logging on startup
@app.on_event("startup")
async def startup_event():
    load_dotenv(".env")
    logger.info("Starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down...")
