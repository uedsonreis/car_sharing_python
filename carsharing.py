import uvicorn
from fastapi import FastAPI, HTTPException, Depends

from repositories.models.trip import TripInput, Trip
from repositories.models.car import CarInput, Car
from repositories.schemas import init_session
from repositories.car_repository import CarRepository
from repositories.trip_repository import TripRepository

app = FastAPI(title="Car Sharing")


@app.on_event("startup")
def on_startup():
    init_session()


@app.get("/api/cars")
def index(size: str | None = None, doors: int = None, service: CarRepository = Depends(CarRepository)) -> list[Car]:
    """Return the stored car list."""

    result = service.get_all(size, doors)
    return result


@app.get("/api/cars/{id}")
def get(id: int, service: CarRepository = Depends(CarRepository)) -> Car:
    """Return a stored car by his id."""

    car = service.get_by_id(id)
    if car:
        return car
    else:
        raise HTTPException(status_code=404, detail=f"No car with id {id}.")


@app.post("/api/cars", response_model=Car)
def store(new_car: CarInput, service: CarRepository = Depends(CarRepository)) -> Car:
    """Stored a new car."""

    car = Car.from_orm(new_car)
    return service.create(car)


@app.put("/api/cars/{id}", response_model=Car)
def update(id: int, body: CarInput, service: CarRepository = Depends(CarRepository)) -> Car:
    """Update a stored car by id."""

    car = Car.from_orm(body)
    saved = service.update(id, car)
    if saved:
        return saved
    else:
        raise HTTPException(status_code=404, detail=f"No car with id {id}.")


@app.delete("/api/cars/{id}", status_code=204)
def delete(id: int, service: CarRepository = Depends(CarRepository)) -> None:
    """Remove a stored car by id."""
    removed = service.remove(id)
    if not removed:
        raise HTTPException(status_code=404, detail=f"Could not remove car with id {id}.")


@app.post("/api/cars/{car_id}/trips", response_model=Trip)
def add_trip(car_id: int, body: TripInput, service: TripRepository = Depends(TripRepository)) -> Trip:
    """Store a new trip into a car."""

    trip = Trip.from_orm(body, update={'car_id': car_id})
    trip = service.create(car_id, trip)

    if trip:
        return trip
    else:
        raise HTTPException(status_code=404, detail=f"No car with id {id}.")


if __name__ == "__main__":
    uvicorn.run("carsharing:app", reload=True)
