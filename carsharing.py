import uvicorn, time
from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from controllers.auth_controller import auth
from controllers.home_controller import home
from controllers.cars_controller import cars
from controllers.user_controller import users
from repositories.schemas import init_session

app = FastAPI(title="Car Sharing")

app.include_router(router=home)
app.include_router(prefix="/api", router=cars)
app.include_router(prefix="/api", router=users)
app.include_router(prefix="/api", router=auth)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.on_event("startup")
def on_startup():
    init_session()


@app.middleware("http")
async def add_process_time_header(request: Request, next_call):
    start_time = time.time()
    response = await next_call(request)
    response.headers["X-Process-Time"] = str(time.time() - start_time)
    return response


@app.exception_handler(HTTPException)
async def exception_handler(request: Request, exception: HTTPException):
    return JSONResponse(
        status_code=exception.status_code,
        content={"message": exception.detail}
    )


if __name__ == "__main__":
    uvicorn.run("carsharing:app", reload=True)
