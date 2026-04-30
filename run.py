# author: luedi
import json
import uvicorn

if __name__ == "__main__":
    with open("production.json") as f:
        config = json.load(f)
    host = config.get("host", "0.0.0.0")
    port = config.get("port", 8080)
    uvicorn.run("main:app", host=host, port=port)
