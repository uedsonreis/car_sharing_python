from fastapi import APIRouter, Request, Form, Depends
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from services.car_service import CarService

home = APIRouter()

templates = Jinja2Templates(directory="templates")


@home.get("/", response_class=HTMLResponse)
def home_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@home.post("/search", response_class=HTMLResponse)
def search(request: Request, size: str = Form(...), doors: int = Form(...), service: CarService = Depends(CarService)):
    cars = service.get_all(size, doors)
    return templates.TemplateResponse("search_result.html", {"request": request, "cars": cars})
