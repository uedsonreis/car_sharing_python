import json

from pydantic import BaseModel


class TripInput(BaseModel):
    start: int
    end: int
    description: str


class TripOutput(TripInput):
    id: int


class CarInput(BaseModel):
    size: str
    fuel: str = "electric"
    doors: int
    transmission: str = "auto"


class CarOutput(CarInput):
    id: int
    trips: list[TripOutput] = []


def load_db() -> list[CarOutput]:
    with open("cars.json") as file:
        return [CarOutput.parse_obj(obj) for obj in json.load(file)]
    return []


def save_db(cars: list[CarInput]):
    with open("cars.json", "w") as file:
        json.dump([car.dict() for car in cars], file, indent=4)
