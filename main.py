from fastapi import FastAPI
from src.database import engine
from src.config import config
from src.model import user
from src.router import user_router
import uvicorn


user.Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(user_router.router)


@app.get("/hello/{name}")
async def root(name):
    my_name = name
    return { "message": f"Hello {my_name}"}

if __name__ == "__main__":
    uvicorn.run(app, host=config.host, port=config.port)
