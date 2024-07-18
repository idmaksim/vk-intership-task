import json
import sys

template = '''from fastapi import FastAPI, HTTPException
import uuid

app = FastAPI()

database = {{}}

{configuration_routes}

{settings_routes}

@app.put("/{{kind}}/{{uuid}}/state")
async def update_state(kind: str, uuid: str, state_update: dict):
    if uuid not in database:
        raise HTTPException(status_code=404, detail="Item not found")
    database[uuid]['state'] = state_update.get('state')
    return database[uuid]

@app.delete("/{{kind}}/{{uuid}}/")
async def delete_item(kind: str, uuid: str):
    if uuid not in database:
        raise HTTPException(status_code=404, detail="Item not found")
    del database[uuid]
    return {{"detail": "Item deleted"}}

@app.get("/{{kind}}/{{uuid}}")
async def read_item(kind: str, uuid: str):
    if uuid not in database:
        raise HTTPException(status_code=404, detail="Item not found")
    return database[uuid]

@app.get("/{{kind}}/{{uuid}}/state")
async def read_state(kind: str, uuid: str):
    if uuid not in database:
        raise HTTPException(status_code=404, detail="Item not found")
    return {{"state": database[uuid].get('state')}}

@app.post("/{{kind}}/")
async def create_item(kind: str, item: dict):
    uuid = str(uuid.uuid4())
    database[uuid] = item
    return {{"id": uuid}}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''

def create_put_route(kind, uuid, field, subfield):
    route = f'''
@app.put("/{kind}/{uuid}/{field}/{subfield}/")
async def update_{field}_{subfield}(kind: str, uuid: str, value: dict):
    if uuid not in database:
        raise HTTPException(status_code=404, detail="Item not found")
    if '{field}' not in database[uuid]:
        raise HTTPException(status_code=404, detail="{field} not found")
    database[uuid]['{field}']['{subfield}'] = value
    return database[uuid]
'''
    return route

def generate_fastapi_code(json_data, output_path):
    kind = json_data.get("kind", "application")

    configuration_routes = ""
    configuration = json_data.get("configuration", {})
    for key in configuration.keys():
        subfields = configuration[key] if isinstance(configuration[key], dict) else {key: configuration[key]}
        for subfield in subfields:
            configuration_routes += create_put_route(kind, "{uuid}", "configuration", subfield)

    settings_routes = ""
    settings = json_data.get("settings", {})
    for key in settings.keys():
        subfields = settings[key] if isinstance(settings[key], dict) else {key: settings[key]}
        for subfield in subfields:
            settings_routes += create_put_route(kind, "{uuid}", "settings", subfield)

    code = template.replace("{{kind}}", kind)
    code = code.replace("{configuration_routes}", configuration_routes)
    code = code.replace("{settings_routes}", settings_routes)

    with open(output_path, 'w') as f:
        f.write(code)

def main(input_path, output_path):
    with open(input_path, 'r') as f:
        json_data = json.load(f)
    
    generate_fastapi_code(json_data, output_path)
    print(f"FastAPI code generated successfully in {output_path}")

if __name__ == "__main__":
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    main(input_path, output_path)
