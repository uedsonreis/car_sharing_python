from fastapi import Depends
from sqlmodel import Session, select

from repositories.models.car import Car
from repositories.schemas import get_session


class CarRepository:

    session: Session

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_all(self, size: str | None = None, doors: int | None = None) -> list[Car]:
        query = select(Car)
        if size:
            query = query.where(Car.size == size)
        if doors:
            query = query.where(Car.doors >= doors)
        return self.session.exec(query).all()

    def get_by_id(self, id: int):
        return self.session.get(Car, id)

    def create(self, car: Car) -> Car:
        self.session.add(car)
        self.session.commit()
        self.session.refresh(car)
        return car

    def update(self, id: int, car: Car) -> Car:
        saved = self.get_by_id(id)
        if saved:
            car.id = id
            self.session.merge(car)
            self.session.commit()
        return saved

    def remove(self, id: int):
        car = self.get_by_id(id)
        if car:
            self.session.delete(car)
            self.session.commit()
            return True
        else:
            return False
