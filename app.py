from pathlib import Path
import pickle

import pandas as pd
from flask import Flask, render_template, request


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "car_price_model.pkl"

# Load the saved model and preprocessing objects
with MODEL_PATH.open("rb") as file:
    model_data = pickle.load(file)

model = model_data["model"]
encoders = model_data["encoders"]
features = model_data["features"]
categorical_fields = ["brand", "fuel", "seller_type", "transmission", "owner"]
options = {field: list(encoders[field].classes_) for field in categorical_fields}

app = Flask(__name__)


def format_price(value):
    return f"Rs. {value:,.2f}"


@app.route("/")
def home():
    return render_template("index.html", options=options, result=None, error=None)


@app.route("/predict", methods=["POST"])
def predict():
    try:
        values = {}

        for field in categorical_fields:
            value = request.form[field]
            if value not in encoders[field].classes_:
                raise ValueError(f"Invalid value for {field}.")
            values[field] = encoders[field].transform([value])[0]

        numeric_fields = ["km_driven", "mileage", "engine", "max_power", "car_age"]
        for field in numeric_fields:
            values[field] = float(request.form[field])

        input_data = pd.DataFrame([values])[features]
        prediction = model.predict(input_data)[0]

        return render_template(
            "index.html",
            options=options,
            result=format_price(prediction),
            error=None,
        )
    except (KeyError, ValueError) as error:
        return render_template(
            "index.html",
            options=options,
            result=None,
            error=str(error),
        ), 400


if __name__ == "__main__":
    app.run(debug=True)
