# author: luedi
import json
import uvicorn
from logger import setup_logging

if __name__ == "__main__":
    with open("production.json") as f:
        config = json.load(f)

    setup_logging(level=config.get("log_level", "INFO"))

    host = config.get("host", "0.0.0.0")
    port = config.get("port", 8181)
    uvicorn.run("main:app", host=host, port=port)
