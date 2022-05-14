from fastapi import Depends
from sqlmodel import Session

from models.trip import Trip
from repositories.schemas import get_session


class TripRepository:

    session: Session

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def create(self, trip: Trip):
        self.session.add(trip)

        self.session.commit()
        self.session.refresh(trip)
        return trip
