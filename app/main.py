from fastapi import FastAPI, APIRouter

from app.routers import article, agent, emplacement, commande, implantation, reception, mission

app = FastAPI(
    title="A simple WMS",
    description="A simple WMS REST API built with FastAPI, SQLAlchemy, and SQLite",
    version="0.1.0",
)

api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(article.router)
api_v1_router.include_router(agent.router)
api_v1_router.include_router(emplacement.router)
api_v1_router.include_router(commande.router)
api_v1_router.include_router(implantation.router)
api_v1_router.include_router(reception.router)
api_v1_router.include_router(mission.router)

app.include_router(api_v1_router)

@app.get("/")
async def root():
    return {"message": "Welcome to SimpleWMS!"}