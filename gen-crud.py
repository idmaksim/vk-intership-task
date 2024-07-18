import importlib.util
from typing import Type, List
from pydantic import BaseModel
import os


def load_pydantic_models(file_path: str) -> List[Type[BaseModel]]:
    spec = importlib.util.spec_from_file_location("models", file_path)
    models = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(models)
    
    # Collect all Pydantic models
    pydantic_models = [
        getattr(models, attr) for attr in dir(models)
        if isinstance(getattr(models, attr), type) and issubclass(getattr(models, attr), BaseModel) and getattr(models, attr) is not BaseModel
    ]
    
    return pydantic_models


def generate_crud_routes(main_model: Type[BaseModel]) -> str:
    model_name = main_model.__name__
    
    routes_code = f"""
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from uuid import UUID
import os

app = FastAPI()

items = {{}}

@app.post("/{{kind}}/")
async def create_item(kind: str, item: {model_name}):
    item_id = UUID(os.urandom(16).hex())
    items[item_id] = jsonable_encoder(item)
    return JSONResponse(status_code=201, content={{"id": item_id, "item": items[item_id]}})

@app.put("/{{kind}}/{{uuid}}/{{field}}/")
async def update_item_field(kind: str, uuid: UUID, field: str, value: str):
    if uuid not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    if field not in items[uuid]:
        raise HTTPException(status_code=400, detail="Field not found in item")
    items[uuid][field] = value
    return items[uuid]

@app.put("/{{kind}}/{{uuid}}/state/")
async def update_item_state(kind: str, uuid: UUID, state: dict):
    if uuid not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    items[uuid]['state'] = state
    return items[uuid]

@app.delete("/{{kind}}/{{uuid}}/")
async def delete_item(kind: str, uuid: UUID):
    if uuid not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    del items[uuid]
    return JSONResponse(status_code=204, content={{}})

@app.get("/{{kind}}/{{uuid}}/")
async def read_item(kind: str, uuid: UUID):
    if uuid not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[uuid]

@app.get("/{{kind}}/{{uuid}}/state/")
async def read_item_state(kind: str, uuid: UUID):
    if uuid not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[uuid].get('state', {{}})
"""

    return routes_code


def create_crud_file(models_file: str, output_file: str):
    main_model = load_pydantic_models(models_file)[-1]  # Assuming the main model is the last one
    routes_code = generate_crud_routes(main_model)
    
    with open(output_file, 'w') as f:
        f.write(routes_code)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python generate_crud.py <path_to_pydantic_models> <output_file>")
        sys.exit(1)
    
    models_file_path = sys.argv[1]
    output_file_path = sys.argv[2]
    create_crud_file(models_file_path, output_file_path)
    print(f"CRUD routes have been written to {output_file_path}")
