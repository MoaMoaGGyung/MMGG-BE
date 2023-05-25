from typing import Union

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello" : "World"}

@app.get("/items/{item_id}")
# A "path" is also commonly called an "endpoint" or a "route".
# "path" is the main way to separate "concerns" and "resources".
def read_item(item_id: int, q: Union[str, None] = None):
    #Union 여러개의 타입 허ㅇ
    return {"item_id": item_id, "q": q}
