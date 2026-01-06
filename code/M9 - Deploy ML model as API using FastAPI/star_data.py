from pydantic import BaseModel, Field   

class StarProperties(BaseModel):
    temperature: int = Field(description="Temperature in Kelvin", example=2376)
    luminosity: float = Field(description="Luminosity in Solar Luminosity", example=0.00073)
    radius: float = Field( description="Radius in Solar Radius", example=0.127)
    abs_mag: float = Field(description="Absolute Magnitude", example=17.22)


pred_prob_example = {
    "Brown Dwarf": 0.6588668588268463,
    "Hypergiant": 0.0010894578637846593,
    "Main Sequence": 0.005465854764863855,
    "Red Dwarf": 0.26195464795013196,
    "Supergiant": 0.0010449570211609447,
    "White Dwarf": 0.0715782237321225
}

class StarTypePrediction(BaseModel):
    predict_probabilities: dict = Field(description="predicted probabilities for allc lasses.",
    example=pred_prob_example)
    predicted_class: str = Field(descripion="Predicted class based on the highest probability.",
    example="Brown Dwarf")
    confidence_score: str = Field(description="Confidence score indicating model's certainty in the predicted class.",
    example="65.9%")