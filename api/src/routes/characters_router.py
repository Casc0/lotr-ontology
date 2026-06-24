from api.src.models import ontology
from fastapi import APIRouter
from api.src.controllers.character_controller import *


router = APIRouter(prefix="/characters", tags=["characters"]) 

@router.get("/{name}")
async def get_characters(name: str):
    return get_character(ontology, name)
    