from pydantic import BaseModel

class Address(BaseModel):
    city: str
    state: str
    pin: str

class Patient(BaseModel):
    name: str
    age: int
    gender: str
    address: Address 


address_dict = {'city': 'TPHCM', 'state': 'Cao Thang', 'pin': '9999'}

address1 = Address(**address_dict)

patient_dict = {'name': 'Khuong', 'gender': 'male', 'age': 27, 'address': address1}

patient1 = Patient(**patient_dict)
print(patient1)