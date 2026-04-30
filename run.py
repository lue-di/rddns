# author: luedi
# date: 2025-08-05 21:14
import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)