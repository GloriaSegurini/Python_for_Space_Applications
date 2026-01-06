from fastapi import FastAPI
from predictor import load_model, make_predictions
import numpy as np
import warnings 
warnings.filterwarnings("ignore")
from star_data import StarProperties, StarTypePrediction

app = FastAPI()

@app.get("/")
def index_route():
    return {"Health": "OK"}


@app.post("/predict", response_model=StarTypePrediction)
def prediction(sp: StarProperties):
    input_features = [[sp.temperature, sp.luminosity, sp.radius, sp.abs_mag]]
    model = load_model("pipeline.pkl")
    predicted_class, probs, classes = make_predictions(model, input_features)
    return {
        'predicted_probabilities': dict(zip (classes, probs)),
        'predicted_class': predicted_class,
        'confidence_score': str(round(np.max(probs), 3)) + '%'
    }