from flask import Flask, request, jsonify
from flask.logging import create_logger
import logging

import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
LOG = create_logger(app)
LOG.setLevel(logging.INFO)

def scale(payload):
    """Scales Payload"""
    try:
        LOG.info("Scaling Payload: %s", payload)
        scaler = StandardScaler().fit(payload)
        scaled_adhoc_predict = scaler.transform(payload)
        return scaled_adhoc_predict
    except ValueError as e:  # Catch only ValueErrors for invalid input data
        LOG.info("Error while scaling payload: %s", e)
        raise

@app.route("/")
def home():
    html = "<h3>Sklearn Prediction Home</h3>"
    # html = "<h2> Sklearn Prediction Home APP - REST API</h2>"    
    return html.format(format)

# TO DO:  Log out the prediction value
@app.route("/predict", methods=['POST'])
def predict():
    # Performs an sklearn prediction
    try:
        clf = joblib.load("./Housing_price_model/LinearRegression.joblib")
        # clf = joblib.load("./Housing_price_model/StochasticGradientDescent.joblib")
        # clf = joblib.load("./Housing_price_model/GradientBoostingRegressor.joblib")
    except FileNotFoundError as e:
        LOG.info("Model file not found: %s", e)
        return "Model not loaded"
    except Exception as e:
        LOG.info("An error occurred while loading the model: %s", e)
        return "Model not loaded"


    json_payload = request.json
    LOG.info(f"JSON payload: {json_payload}")
    inference_payload = pd.DataFrame(json_payload)
    LOG.info(f"inference payload DataFrame: {inference_payload}")
    scaled_payload = scale(inference_payload)
    prediction = list(clf.predict(scaled_payload))
    return jsonify({'prediction': prediction})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
