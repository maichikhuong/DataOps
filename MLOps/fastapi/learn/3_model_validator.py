from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, model_validator
from typing import List, Dict, Optional, Annotated


class Patient(BaseModel):
    name: str
    age: int 
    email: EmailStr
    link_url: AnyUrl
    weight: float
    married: bool
    allergies: List[str] = None
    contact_details: Dict[str, str]

    @model_validator(mode='after')
    def validate_emergency_contact(cls, model):
        if model.age > 60 and 'emergency' not in model.contact_details:
            raise ValueError('Patients older the 60 must have an emrgency contact')
        return model


def insert_data(patient: Patient):
    print(patient)
    print('Insert data successfully!')

# insert_data('Khuong', '28')
patient_info = {'name': 'Khuong', 'age': '65', 'email': 'khuong@icici.com', 'link_url': 'https://www.linkedin.com/in/khuong-mai-chi-4b917b1bb/'
                , 'weight': 80, 'married': True, 'contact_details': {'email': 'abc@gmail.com', 'phone': '123456'}}

patient1 = Patient(**patient_info) #validation -> type coercion

insert_data(patient1)