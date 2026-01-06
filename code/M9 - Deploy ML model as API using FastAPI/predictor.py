import pickle


# Load trained model
def load_model(model_path):
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    return model

# Define prediction function
def make_predictions(model, input_features):
    predict_class = model.predict(input_features)[0]
    probabilities = model.predict_proba(input_features)[0]
    classes = model.classes_    
    return predict_class, probabilities, classes



    