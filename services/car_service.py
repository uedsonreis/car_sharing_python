from fastapi import Depends

from repositories.car_repository import CarRepository
from models.car import Car


class CarService:
    repository: CarRepository

    def __init__(self, repository: CarRepository = Depends(CarRepository)):
        self.repository = repository

    def get_all(self, size: str | None = None, doors: int = None):
        return self.repository.get_all(size, doors)

    def get_by_id(self, id: int):
        return self.repository.get_by_id(id)

    def create(self, car: Car):
        return self.repository.create(car)

    def update(self, id: int, car: Car):
        return self.repository.update(id, car)

    def remove(self, id: int):
        return self.repository.remove(id)
