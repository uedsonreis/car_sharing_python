import uvicorn
from fastapi import FastAPI, HTTPException

from schemas import CarInput, CarOutput, load_db, save_db

app = FastAPI()

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


@app.post("/api/cars")
def store(car: CarInput) -> CarOutput:
    new_car = CarOutput(size=car.size, doors=car.doors, fuel=car.fuel, transmission=car.transmission, id=len(db)+1)
    db.append(new_car)
    save_db(db)
    return new_car


if __name__ == "__main__":
    uvicorn.run("carsharing:app", reload=True)
