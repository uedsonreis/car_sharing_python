import uvicorn
from fastapi import FastAPI, HTTPException

from schemas import CarInput, CarOutput, TripInput, TripOutput, load_db, save_db

app = FastAPI(title="Car Sharing")

db = load_db()


@app.get("/api/cars")
def index(size: str | None = None, doors: int = None) -> list[CarOutput]:
    """Return the stored car list."""
    result = db

    if size:
        result = [car for car in result if car.size == size]
    if doors:
        result = [car for car in result if car.doors >= doors]

    return result


@app.get("/api/cars/{id}")
def get(id: int) -> CarOutput:
    """Return a stored car by his id."""

    result = [car for car in db if car.id == id]
    if result:
        return result[0]
    else:
        raise HTTPException(status_code=404, detail=f"No car with id {id}.")


@app.post("/api/cars", response_model=CarOutput)
def store(car: CarInput) -> CarOutput:
    new_car = CarOutput(size=car.size, doors=car.doors, fuel=car.fuel, transmission=car.transmission, id=len(db)+1)
    db.append(new_car)
    save_db(db)
    return new_car


@app.put("/api/cars/{id}", response_model=CarOutput)
def update(id: int, body: CarInput) -> CarOutput:
    car = get(id)

    car.size = body.size
    car.fuel = body.fuel
    car.doors = body.doors
    car.transmission = body.transmission

    save_db(db)
    return car


@app.delete("/api/cars/{id}", status_code=204)
def delete(id: int) -> None:
    car = get(id)
    db.remove(car)
    save_db(db)


@app.post("/api/cars/{car_id}/trips", response_model=TripOutput)
def addTrip(car_id: int, trip: TripInput) -> TripOutput:
    car = get(car_id)
    new_trip = TripOutput(id=len(car.trips)+1, start=trip.start, end=trip.end, description=trip.description)
    car.trips.append(new_trip)

    save_db(db)
    return new_trip


if __name__ == "__main__":
    uvicorn.run("carsharing:app", reload=True)
