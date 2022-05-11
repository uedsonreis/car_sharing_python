from sqlmodel import SQLModel, Field, Relationship


class TripInput(SQLModel):
    start: int
    end: int
    description: str

    class Config:
        schema_extra = {
            "example": {
                "start": 1, "end": 2, "description": "qualquer"
            }
        }


class Trip(TripInput, table=True):
    id: int | None = Field(primary_key=True, default=None)
    car_id: int = Field(foreign_key="car.id")
    car: "Car" = Relationship(back_populates="trips")
