from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, model_validator, computed_field
from typing import List, Dict, Optional, Annotated, Literal


class PredictionResponse(BaseModel):
    predicted_category: Annotated[str, Field(
        ..., description='The predicted insurance premium category', example='High')]

    confidence: Annotated[float, Field(
        ..., description="Model's confidence score of the predicted class (range: 0 to 1)", example=0.84)]

    class_probabilities: Annotated[Dict[str, float], Field(
        ...,
        description="Probability distribution across all possible classes",
        example={"Low": 0.01, "Medium": 0.15, "High": 0.84}
    )]
