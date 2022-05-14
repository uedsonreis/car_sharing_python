from sqlmodel import SQLModel, Field, Relationship

from models.trip import Trip


class CarInput(SQLModel):
    size: str
    fuel: str = "electric"
    doors: int
    transmission: str = "auto"

    class Config:
        schema_extra = {
            "example": {
                "size": "m", "doors": 5, "transmission": "manual", "fuel": "hybrid"
            }
        }


class Car(CarInput, table=True):
    id: int | None = Field(primary_key=True, default=None)
    trips: list[Trip] = Relationship(back_populates="car")
