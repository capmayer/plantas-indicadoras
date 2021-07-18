from sqlalchemy import Column, Integer, String
from .database import Base
from slugify import slugify


def slugify_name(context):
    scientific_name = context.get_current_parameters()["scientific_name"]
    return slugify(scientific_name)


class Plant(Base):
    __tablename__ = "plants"

    id = Column(Integer, primary_key=True, index=True)
    scientific_name = Column(String, unique=True, index=True)
    scientific_name_slug = Column(String, unique=True, default=slugify_name)
    popular_names = Column(String)
    indicates = Column(String)
    description = Column(String)


