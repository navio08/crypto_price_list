import uvicorn

from app import coinmarketApp  # noqa

if __name__ == "__main__":
    uvicorn.run("main:coinmarketApp", reload=True)
