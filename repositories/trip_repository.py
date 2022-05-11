from fastapi import Depends
from sqlmodel import Session

from repositories.models.car import Car
from repositories.models.trip import Trip
from repositories.schemas import get_session


class TripRepository:

    session: Session

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def create(self, car_id: int, trip: Trip):
        car = self.session.get(Car, car_id)
        if not car:
            return None

        trip.car_id = car.id
        self.session.add(trip)

        self.session.commit()
        self.session.refresh(trip)
        return trip
