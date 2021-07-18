import secrets
from typing import List

from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
# from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi import status

from plants import models, schemas, crud
from plants.database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


security = HTTPBasic()


@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request, db: Session = Depends(get_db)):
    plants = crud.get_plants(db)
    return templates.TemplateResponse("index.html", {"request": request, "plants": plants})


@app.get("/api/plants", response_model=List[schemas.Plant])
async def get_plants(db: Session = Depends(get_db)):
    plants = crud.get_plants(db)
    return plants


@app.get("/{scientific_name}", response_class=HTMLResponse)
async def get_plant(scientific_name: str, request: Request, db: Session = Depends(get_db)):
    plant = crud.get_plant_by_name(db, scientific_name=scientific_name)

    if plant:
        return templates.TemplateResponse("plant.html", {"request": request, "plant": plant})
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Plant don't exist!")


@app.post("/api/plants", response_model=schemas.Plant)
async def create_plant(
    plant: schemas.PlantBase,
    db: Session = Depends(get_db),
    credentials: HTTPBasicCredentials = Depends(security)
):
    correct_username = secrets.compare_digest(credentials.username, "stanleyjobson")
    correct_password = secrets.compare_digest(credentials.password, "swordfish")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    db_plant = crud.get_plant_by_name(db, plant.scientific_name)
    if db_plant:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Plant already created!")
    else:
        new_plant = crud.create_plant(db, plant)
        return new_plant
