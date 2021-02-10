from enum import Enum
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


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
async def read_item(
            item_id: int,
            q: Optional[str] = None,
            short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {
                "description": ("This is an amazing "
                                "item that has a long description")
            }
        )
    return item


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {
            "model_name": model_name,
            "message": "LeCNN all images"
            }

    return {
        "model_name": model_name,
        "message": "Have some residuals"
        }


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


@app.get("/items/")
async def query_with_defaults(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]


@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: Optional[str] = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result
