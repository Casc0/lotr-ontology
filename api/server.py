from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.src.routes import character_router, faction_router, place_router, race_router
from api.src.models import Ontology

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.ontology = Ontology()
    yield

app = FastAPI(
    title="fastapi-lotr-ontology",
    description="A lotr ontology API",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(character_router, prefix="/api")
app.include_router(faction_router, prefix="/api")
app.include_router(place_router, prefix="/api")
app.include_router(race_router, prefix="/api")

@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}