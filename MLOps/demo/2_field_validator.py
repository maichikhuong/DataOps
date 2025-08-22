from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator
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

    @field_validator('email')
    @classmethod
    def email_validator(cls, value):
        valid_domains = ['hdfc.com', 'icici.com']
        # abc@gmail.com
        domain_name = value.split('@')[-1]
        if domain_name not in valid_domains:
            raise ValueError('Not a valid domain')
        return value
    
    @field_validator('name', mode='after')
    @classmethod
    def transform_name(cls, value):
        return value.upper()

def insert_data(patient: Patient):
    print(patient)
    print('Insert data successfully!')

# insert_data('Khuong', '28')
patient_info = {'name': 'Khuong', 'age':27, 'email': 'khuong@icici.com', 'link_url': 'https://www.linkedin.com/in/khuong-mai-chi-4b917b1bb/'
                , 'weight': 80, 'married': True, 'contact_details': {'email': 'abc@gmail.com', 'phone': '123456'}}

patient1 = Patient(**patient_info) #validation -> type coercion

insert_data(patient1)