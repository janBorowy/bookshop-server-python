from fastapi import FastAPI;
from src.database import engine
from src.config import config
from src import model
import uvicorn


model.Base.metadata.create_all(bind=engine)


app = FastAPI()

@app.get("/hello/{name}")
async def root(name):
    my_name = name
    return { "message": f"Hello {my_name}"}

if __name__ == "__main__":
    uvicorn.run(app, host=config.host, port=config.port)