from enum import Enum
from typing import Optional
from fastapi import FastAPI


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


app = FastAPI()

fake_items_db = [
    {"item_one": "One"},
    {"item_two": "Two"},
    {"item_three": "Three"},
    {"item_four": "Four"},
    {"item_five": "Five"},
    {"item_six": "Six"},
]


@app.get("/")
def read_root():
    return {"Hello", "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


@app.get("/items/")
async def query_with_defaults(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]
