from fastapi import FastAPI
from src.database import engine
from src.config import config
from src.model import bookshop_model, user
from src.router import author_router, book_router, user_router
from src.security.login_security import token_router
import uvicorn

bookshop_model.Base.metadata.create_all(bind=engine)
user.Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(user_router.router)
app.include_router(token_router)
app.include_router(author_router.router)
app.include_router(book_router.router)


if __name__ == "__main__":
    uvicorn.run(app, host=config.host, port=config.port)
