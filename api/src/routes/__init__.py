from .characters_router import router as character_router
from .factions_router import router as faction_router
from .places_router import router as place_router
from .races_router import router as race_router

__all__ = ["character_router", "faction_router", "place_router", "race_router"]