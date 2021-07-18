from pydantic import BaseModel


class PlantBase(BaseModel):
    scientific_name: str
    popular_names: str
    description: str
    indicates: str


class PlantList(PlantBase):
    scientific_name_slug: str


class Plant(PlantList):
    id: int

    class Config:
        orm_mode = True
