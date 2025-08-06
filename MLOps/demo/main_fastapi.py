from fastapi import FastAPI
import json

app = FastAPI()

def load_data():
    with open('partient.json', 'r') as f:
        data = json.load(f)

    return data

@app.get("/")
def hello():
    return {'message': 'Hello world'}


@app.get("/about")
def about():
    return {'message': 'CampusX is an education'}


@app.get("/view")
def view ():
    data = load_data()
    return data