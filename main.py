from fastapi import FastAPI;
import uvicorn

app = FastAPI()

@app.get("/hello/{name}")
async def root(name):
    my_name = name
    return { "message": f"Hello {my_name}"}

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8080)