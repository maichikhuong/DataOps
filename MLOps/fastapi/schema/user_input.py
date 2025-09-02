from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, model_validator, computed_field
from typing import List, Dict, Optional, Annotated, Literal
# import city tigers
from config.city_tigers import tier_1_cities, tier_2_cities

class UserInput(BaseModel):
    age: Annotated[int, Field(..., gt=0, lt=120,
                              description='Age of the user')]
    weight: Annotated[float,
                      Field(..., gt=0, description='Weight of the user')]
    height: Annotated[float,
                      Field(..., gt=0, lt=2.5, description='Height of the user')]
    income_lpa: Annotated[float,
                          Field(..., gt=0, description='Annual Salary of the user')]
    smoker: Annotated[bool, Field(..., description='Is user a smoker')]
    city: Annotated[str, Field(..., description='City of the user')]
    occupation: Annotated[Literal['retired', 'freelancer', 'student', 'government_job',
                                  'business_owner', 'unemployed', 'private_job'], Field(..., description='Occupation of the user')]

    @field_validator('city')
    @classmethod
    def normalize_city(cls, v: str) -> Annotated[str, any]:
        v = v.strip().title()
        return v

    @computed_field
    @property
    def bmi(self) -> Annotated[float, Field(..., examples='Feature Engineering')]:
        return self.weight/(self.height**2)

    @computed_field
    @property
    def lifestyle_risk(self) -> Annotated[str, Field(..., examples='Feature Engineering')]:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return "low"

    @computed_field
    @property
    def age_group(self) -> Annotated[str, Field(..., examples='Feature Engineering')]:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "senior"

    @computed_field
    @property
    def city_tier(self) -> Annotated[int, Field(..., examples='Feature Engineering')]:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3