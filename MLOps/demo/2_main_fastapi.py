from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, model_validator, computed_field
from typing import List, Dict, Optional, Annotated, Literal

app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description='ID of the patient', examples=['P001'])]
    name: Annotated[str, Field(..., description='Name of the patient', examples=['Ananya Verma'])]
    city: Annotated[str, Field(..., description='City where the patient is living', examples=['Guwahati'])]
    age: Annotated[int, Field(..., gt = 0, lt = 120, description='Age of the patient', examples=[27])]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description='Age of the patient')]
    height: Annotated[float, Field(..., gt = 0, description = 'Height of the patient')]
    weight: Annotated[float, Field(..., gt = 0, description = 'Height of the patient')]

    @computed_field
    @property
    def bmi(self) -> Annotated[float, any]:
        bmi = round(self.weight/(self.height**2), 2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> Annotated[str, any]:
        if self.bmi < 18.5:
            return 'UnderWeight'
        elif self.bmi < 30:
            return 'Normal'
        else:
            return 'Obese'

def load_data():
    with open('partient_02.json', 'r') as f:
        data = json.load(f)

    return data 

def save_data(data):
    with open('partient_02.json', 'w') as f:
        json.dump(data, f)

@app.get("/")
def hello():
    return {'message': 'Patient Management System API'}        

@app.post("/create")
def create_patient(patient: Patient):
    # load existing data
    data = load_data()

    # check if the patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exists')
    
    # new patient add to the database
    data[patient.id] = patient.model_dump(exclude=['id'])

    # save data
    save_data(data)

    return JSONResponse(status_code=201, content={'message': 'patient created success'})