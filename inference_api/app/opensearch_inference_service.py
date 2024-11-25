from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import pandas as pd

# Create a FastAPI application instance
app = FastAPI()

# Load the pre-trained machine learning model
with open('/code/model/regression_model.pkl', 'rb') as fid:
    model = pickle.load(fid)

# Define a Pydantic model for input validation
class InputData(BaseModel):
    data: str

# Define a POST endpoint for making predictions
@app.post("/predict/")
def predict(input_data: InputData):
    """
    Accept a JSON object with a key "data" containing a comma-separated string of floats.
    Convert the string to a list of floats and use the model to make predictions.
    """
    try:
        # Split the input string by commas and convert to a list of floats
        data_list = [float(value.strip()) for value in input_data.data.split(",")]

        # Define the column names for the input features
        columns = model.feature_names_in_

        # Create a pandas DataFrame from the input data
        features = pd.DataFrame([data_list], columns=columns)

        # Use the model to make a prediction
        prediction = round(model.predict(features)[0], 2)
        keywordness = 1 - prediction

        # Return the prediction as a JSON object
        return {
            "neuralness": prediction,
            "keywordness": keywordness
        }

    except Exception as e:
        # Handle errors and provide feedback
        return {"error": str(e)}
