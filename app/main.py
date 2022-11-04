from fastapi import Depends, FastAPI, HTTPException, status
from fastapi_utils.tasks import repeat_every
from app.utils.job import job
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, base_season_pond, base_season, user, unit, address, adopt, supplier, pond, medicine, environment, disease, food, \
    equipment, fish_original, harmful_animal, pond_type, pond_category, supplier_type, adopt_type, medicine_out,\
    medicine_in, food_in, food_out, measure_index, water_diary, dead_fish_diary, image, purchasing_dealer, \
    collect_season, clean_season, water_index_season, chemistry, environment_renovation, chemistry_in, chemistry_out, \
    shape , food_type , chemistry_type, medicine_type, specification , fish_type

from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

import secrets
from fastapi.security import HTTPBasic, HTTPBasicCredentials


app = FastAPI(
     title="Nghề nông việt api",
    version="0.1.0",
    docs_url=None,
    redoc_url=None,
    openapi_url = None
)


security = HTTPBasic()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "dev@nghenongviet.vn")
    correct_password = secrets.compare_digest(credentials.password, "dev_doc@password")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/docs", include_in_schema=False)
async def get_swagger_documentation(username: str = Depends(get_current_username)):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")


@app.get("/redoc", include_in_schema=False)
async def get_redoc_documentation(username: str = Depends(get_current_username)):
    return get_redoc_html(openapi_url="/openapi.json", title="docs")


@app.get("/openapi.json", include_in_schema=False)
async def openapi(username: str = Depends(get_current_username)):
    return get_openapi(title=app.title, version=app.version, routes=app.routes)

# @app.on_event("startup")
# @repeat_every(seconds=60, raise_exceptions=True)
# def auto_created():
#     job()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(unit.router)
app.include_router(address.router)
app.include_router(adopt.router)
app.include_router(adopt_type.router)
app.include_router(supplier.router)
app.include_router(supplier_type.router)
app.include_router(pond.router)
app.include_router(pond_type.router)
app.include_router(pond_category.router)
app.include_router(environment.router)
app.include_router(disease.router)
app.include_router(equipment.router)
app.include_router(harmful_animal.router)
app.include_router(fish_original.router)
app.include_router(fish_type.router)
app.include_router(food.router)
app.include_router(food_type.router)
app.include_router(food_in.router)
app.include_router(food_out.router)
app.include_router(medicine.router)
app.include_router(medicine_type.router)
app.include_router(medicine_in.router)
app.include_router(medicine_out.router)
app.include_router(measure_index.router)
app.include_router(water_diary.router)
app.include_router(dead_fish_diary.router)
app.include_router(image.router)
app.include_router(base_season.router)
app.include_router(base_season_pond.router)
app.include_router(collect_season.router)
app.include_router(clean_season.router)
app.include_router(water_index_season.router)
app.include_router(purchasing_dealer.router)
app.include_router(environment_renovation.router)
app.include_router(chemistry.router)
app.include_router(chemistry_type.router)
app.include_router(chemistry_in.router)
app.include_router(chemistry_out.router)
app.include_router(shape.router)
app.include_router(specification.router)


@app.get("/")
def root():
    return "NNV apis"

