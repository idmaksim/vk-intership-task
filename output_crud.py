from fastapi import FastAPI, HTTPException
import uuid

app = FastAPI()

database = {{}}


@app.put("/application/{uuid}/configuration/jvmConfig/")
async def update_configuration_jvmConfig(kind: str, uuid: str, value: dict):
    if uuid not in database:
        raise HTTPException(status_code=404, detail="Item not found")
    if 'configuration' not in database[uuid]:
        raise HTTPException(status_code=404, detail="configuration not found")
    database[uuid]['configuration']['jvmConfig'] = value
    return database[uuid]

@app.put("/application/{uuid}/configuration/exposedPorts/")
async def update_configuration_exposedPorts(kind: str, uuid: str, value: dict):
    if uuid not in database:
        raise HTTPException(status_code=404, detail="Item not found")
    if 'configuration' not in database[uuid]:
        raise HTTPException(status_code=404, detail="configuration not found")
    database[uuid]['configuration']['exposedPorts'] = value
    return database[uuid]

@app.put("/application/{uuid}/configuration/sharedNamespace/")
async def update_configuration_sharedNamespace(kind: str, uuid: str, value: dict):
    if uuid not in database:
        raise HTTPException(status_code=404, detail="Item not found")
    if 'configuration' not in database[uuid]:
        raise HTTPException(status_code=404, detail="configuration not found")
    database[uuid]['configuration']['sharedNamespace'] = value
    return database[uuid]


@app.put("/application/{{uuid}}/state")
async def update_state(kind: str, uuid: str, state_update: dict):
    if uuid not in database:
        raise HTTPException(status_code=404, detail="Item not found")
    database[uuid]['state'] = state_update.get('state')
    return database[uuid]

@app.delete("/application/{{uuid}}/")
async def delete_item(kind: str, uuid: str):
    if uuid not in database:
        raise HTTPException(status_code=404, detail="Item not found")
    del database[uuid]
    return {{"detail": "Item deleted"}}

@app.get("/application/{{uuid}}")
async def read_item(kind: str, uuid: str):
    if uuid not in database:
        raise HTTPException(status_code=404, detail="Item not found")
    return database[uuid]

@app.get("/application/{{uuid}}/state")
async def read_state(kind: str, uuid: str):
    if uuid not in database:
        raise HTTPException(status_code=404, detail="Item not found")
    return {{"state": database[uuid].get('state')}}

@app.post("/application/")
async def create_item(kind: str, item: dict):
    uuid = str(uuid.uuid4())
    database[uuid] = item
    return {{"id": uuid}}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
