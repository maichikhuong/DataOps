from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    name: Annotated[str, Field(max_length = 50, title='Name of the patient', description='Give the name of the patient in less than 50 chars', examples=['Khuong', 'Kien'])]
    age: int = Field(gt = 0, lt = 100)
    email: EmailStr
    link_url: AnyUrl
    weight: Annotated[float, Field(gt = 0, strict=True)]
    married: Annotated[bool, Field(default=None, description='Is the patient married or not')]
    allergies: Annotated[Optional[List[str]], Field(default=None, max_length=5)]
    contact_details: Dict[str, str]

def insert_data(patient: Patient):
    # # print(name)
    # # print(age)
    # # print('Insert data successfully!')
    # if type(name) == str and type(age) == int:
    #     print(name)
    #     print(age)
    #     print('Insert data successfully!')
    # else:
    #     raise TypeError("Incorrect data type")
    print(patient.name)
    print(patient.age)
    print(patient.email)
    print(patient.allergies)
    print(patient.married)
    print(patient.email)
    print(patient.link_url)
    print('Insert data successfully!')
        

# insert_data('Khuong', '28')
patient_info = {'name': 'Khuong', 'age':27, 'email': 'khuong@acb.com.vn', 'link_url': 'https://www.linkedin.com/in/khuong-mai-chi-4b917b1bb/'
                , 'weight': 80, 'contact_details': {'email': 'abc@gmail.com', 'phone': '123456'}}

patient1 = Patient(**patient_info)

insert_data(patient1)