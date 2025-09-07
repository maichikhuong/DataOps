from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, model_validator, computed_field
from typing import List, Dict, Optional, Annotated


class Patient(BaseModel):
    name: str
    age: int 
    email: EmailStr
    link_url: AnyUrl
    weight: float # kg
    height: float # mtr
    married: bool
    allergies: List[str] = None
    contact_details: Dict[str, str]

    @computed_field
    @property
    def calculate_bmi(self) -> float:
        bmi = round(self.weight / (self.height ** 2), 2)
        return bmi

def insert_data(patient: Patient):
    print(patient.age)
    print(patient.calculate_bmi)
    print('Insert data successfully!')

# insert_data('Khuong', '28')
patient_info = {'name': 'Khuong', 'age': '65', 'email': 'khuong@icici.com', 'link_url': 'https://www.linkedin.com/in/khuong-mai-chi-4b917b1bb/'
                , 'height': 1.72, 'weight': 80, 'married': True, 'contact_details': {'email': 'abc@gmail.com', 'phone': '123456'}}

patient1 = Patient(**patient_info) #validation -> type coercion

insert_data(patient1)