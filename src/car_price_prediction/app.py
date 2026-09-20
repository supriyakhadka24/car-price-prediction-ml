import pickle
from pathlib import Path

import pandas as pd
from flask import Flask, redirect, render_template, request, url_for

from .config import (
    CATEGORICAL_FIELDS,
    DEFAULT_FORM_VALUES,
    MODEL_PATH,
    NUMERIC_FIELDS,
)


def load_model(model_path: Path):
    with model_path.open("rb") as file:
        return pickle.load(file)


def format_price(value):
    return f"Rs. {value:,.2f}"


def create_app():
    model_data = load_model(MODEL_PATH)
    model = model_data["model"]
    encoders = model_data["encoders"]
    features = model_data["features"]
    options = {
        field: list(encoders[field].classes_) for field in CATEGORICAL_FIELDS
    }

    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
    )

    @app.route("/")
    def home():
        return render_template(
            "index.html",
            options=options,
            result=None,
            error=None,
            form_values=DEFAULT_FORM_VALUES,
        )

    @app.route("/predict", methods=["GET", "POST"])
    def predict():
        if request.method == "GET":
            return redirect(url_for("home"))

        form_values = request.form.to_dict()

        try:
            values = {}

            for field in CATEGORICAL_FIELDS:
                value = request.form[field]
                if value not in encoders[field].classes_:
                    raise ValueError(f"Invalid value for {field}.")
                values[field] = encoders[field].transform([value])[0]

            for field in NUMERIC_FIELDS:
                values[field] = float(request.form[field])

            input_data = pd.DataFrame([values])[features]
            prediction = model.predict(input_data)[0]

            return render_template(
                "index.html",
                options=options,
                result=format_price(prediction),
                error=None,
                form_values=form_values,
            )
        except (KeyError, ValueError) as error:
            return render_template(
                "index.html",
                options=options,
                result=None,
                error=str(error),
                form_values=form_values,
            ), 400

    return app


app = create_app()
