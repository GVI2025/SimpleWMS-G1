from fastapi import FastAPI

from app.routers import article, agent, emplacement, commande, implantation, reception, mission, salle

app = FastAPI(
    title="A simple WMS",
    description="A simple WMS REST API built with FastAPI, SQLAlchemy, and SQLite",
    version="0.1.0",
)

app.include_router(article.router)
app.include_router(agent.router)
app.include_router(emplacement.router)
app.include_router(commande.router)
app.include_router(implantation.router)
app.include_router(reception.router)
app.include_router(mission.router)
app.include_router(salle.router)

@app.get("/")
async def root():
    return {"message": "Welcome to SimpleWMS!"}