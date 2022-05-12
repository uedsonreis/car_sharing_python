import uvicorn
from fastapi import FastAPI

from controllers.home_controller import home
from controllers.cars_controller import cars
from repositories.schemas import init_session

app = FastAPI(title="Car Sharing")
app.include_router(router=home)
app.include_router(prefix="/api", router=cars)


@app.on_event("startup")
def on_startup():
    init_session()


if __name__ == "__main__":
    uvicorn.run("carsharing:app", reload=True)
