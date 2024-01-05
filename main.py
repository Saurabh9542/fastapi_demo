from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()

@app.get("/")
def root():
    return {"Hello": "World"}


@app.get("/posts")
def get_posts():
    return {"data": "Thsi si my post"}


@app.post("/createposts")
def create_posts(payload: dict= Body(...)):
    return {"data": f"title: {payload['title']}"}