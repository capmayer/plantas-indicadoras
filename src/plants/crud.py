from sqlalchemy.orm import Session

from src.plants import models, schemas


def get_plant(db: Session, plant_id: int):
    return db.query(models.Plant).filter(models.Plant.id == plant_id).first()


def get_plant_by_name(db: Session, scientific_name: str):
    return db.query(models.Plant).filter(models.Plant.scientific_name_slug.contains(scientific_name)).first()


def get_plants(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Plant).offset(skip).limit(limit).all()


def create_plant(db: Session, plant: schemas.PlantBase):
    new_plant = models.Plant(**plant.dict())
    db.add(new_plant)
    db.commit()
    db.refresh(new_plant)
    return new_plant
