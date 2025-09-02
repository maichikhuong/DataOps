from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, model_validator, computed_field
from typing import List, Dict, Optional, Annotated, Literal

app = FastAPI()


class Patient(BaseModel):
    id: Annotated[str,
                  Field(..., description='ID of the patient', examples=['P001'])]
    name: Annotated[str, Field(..., description='Name of the patient', examples=[
                               'Ananya Verma'])]
    city: Annotated[str, Field(..., description='City where the patient is living', examples=[
                               'Guwahati'])]
    age: Annotated[int, Field(..., gt=0, lt=120,
                              description='Age of the patient', examples=[27])]
    gender: Annotated[Literal['male', 'female', 'others'],
                      Field(..., description='Age of the patient')]
    height: Annotated[float,
                      Field(..., gt=0, description='Height of the patient')]
    weight: Annotated[float,
                      Field(..., gt=0, description='Height of the patient')]

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


class PatientUpdate(BaseModel):
    id: Annotated[Optional[str], Field(default=None)]
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0, lt=120)]
    gender: Annotated[Optional[Literal['male',
                                       'female', 'others']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]


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


@app.put("/edit/{patient_id}")
def update_patient(patient_id: str, patient_update: PatientUpdate):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    existing_patient_info = data[patient_id]

    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value

    # existing_patient_info -> pydantic object -> update bmi -> verdict
    existing_patient_info['id'] = patient_id
    patient_pydantic_obj = Patient(**existing_patient_info)
    # -> pydantic object -> dict
    existing_patient_info = patient_pydantic_obj.model_dump(exclude='id')

    # add this dict to data
    data[patient_id] = existing_patient_info

    # save data
    save_data(data)

    return JSONResponse(status_code=201, content={'message': 'patient updated'})

@app.delete("/delete/{patient_id}")
def update_patient(patient_id: str):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')

    del data[patient_id]

    # save data
    save_data(data)

    return JSONResponse(status_code=201, content={'message': 'patient deleted'})