from pydantic import BaseModel

class BusCreate(BaseModel):
    bus_number: str
    route: str
    latitude: float
    longitude: float
