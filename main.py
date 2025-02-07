import fastapi
import uvicorn

from config import Config


app = fastapi.FastAPI()
config = Config("config.json")


if __name__ == "__main__":
	uvicorn.run(app=app, host="0.0.0.0", port=8000, reload=True)
