import uvicorn
from fastapi import FastAPI

import controllers.todos

app = FastAPI()

app.include_router(controllers.todos.router)


if __name__ == '__main__':
    uvicorn.run('main:app', port=8083)