from fastapi import Depends

from repositories.car_repository import CarRepository
from repositories.trip_repository import TripRepository
from models.trip import Trip


class TripService:
    repository: TripRepository
    carRepository: CarRepository

    def __init__(self, repository: TripRepository = Depends(TripRepository), car_repository: CarRepository = Depends(CarRepository)):
        self.repository = repository
        self.carRepository = car_repository

    def create(self, car_id: int, trip: Trip):
        car = self.carRepository.get_by_id(car_id)
        if not car:
            return None

        trip.car_id = car.id
        return self.repository.create(trip)
