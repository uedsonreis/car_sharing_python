from fastapi import HTTPException, Depends, APIRouter

from repositories.models.trip import TripInput, Trip
from repositories.models.car import CarInput, Car
from services.car_service import CarService
from services.trip_service import TripService

cars = APIRouter(prefix="/cars")


@cars.get("")
def index(size: str | None = None, doors: int = None, service: CarService = Depends(CarService)) -> list[Car]:
    """Return the stored car list."""

    result = service.get_all(size, doors)
    return result


@cars.get("/{id}")
def get(id: int, service: CarService = Depends(CarService)) -> Car:
    """Return a stored car by his id."""

    car = service.get_by_id(id)
    if car:
        return car
    else:
        raise HTTPException(status_code=404, detail=f"No car with id {id}.")


@cars.post("", response_model=Car)
def store(new_car: CarInput, service: CarService = Depends(CarService)) -> Car:
    """Stored a new car."""

    car = Car.from_orm(new_car)
    return service.create(car)


@cars.put("/{id}", response_model=Car)
def update(id: int, body: CarInput, service: CarService = Depends(CarService)) -> Car:
    """Update a stored car by id."""

    car = Car.from_orm(body)
    saved = service.update(id, car)
    if saved:
        return saved
    else:
        raise HTTPException(status_code=404, detail=f"No car with id {id}.")


@cars.delete("/{id}", status_code=204)
def delete(id: int, service: CarService = Depends(CarService)) -> None:
    """Remove a stored car by id."""
    removed = service.remove(id)
    if not removed:
        raise HTTPException(status_code=404, detail=f"Could not remove car with id {id}.")


@cars.post("/{car_id}/trips", response_model=Trip)
def add_trip(car_id: int, body: TripInput, service: TripService = Depends(TripService)) -> Trip:
    """Store a new trip into a car."""

    trip = Trip.from_orm(body, update={'car_id': car_id})
    trip = service.create(car_id, trip)

    if trip:
        return trip
    else:
        raise HTTPException(status_code=404, detail=f"No car with id {id}.")
