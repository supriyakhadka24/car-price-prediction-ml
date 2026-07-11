from pathlib import Path
import pickle

import pandas as pd
from flask import Flask, jsonify, render_template, request

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model.pkl"
LEGACY_MODEL_PATH = BASE_DIR / "car_price_model.pkl"
DATA_PATH = BASE_DIR / "data" / "Cardetails.csv"


FIELD_META = {
    "brand": {
        "label": "Brand",
        "type": "select",
        "help": "Choose the manufacturer used by the model encoder.",
    },
    "fuel": {
        "label": "Fuel Type",
        "type": "select",
        "help": "Petrol, diesel, LPG, or CNG.",
    },
    "seller_type": {
        "label": "Seller Type",
        "type": "select",
        "help": "Dealer, individual, or trustmark dealer.",
    },
    "transmission": {
        "label": "Transmission",
        "type": "select",
        "help": "Automatic or manual gearbox.",
    },
    "owner": {
        "label": "Ownership",
        "type": "select",
        "help": "Select the ownership history of the car.",
    },
    "km_driven": {
        "label": "Kilometers Driven",
        "type": "number",
        "step": "1",
        "min": "0",
        "help": "Total distance covered by the car.",
    },
    "mileage": {
        "label": "Mileage (km/l)",
        "type": "number",
        "step": "0.1",
        "min": "0",
        "help": "Use the mileage value without the km/l suffix.",
    },
    "engine": {
        "label": "Engine Capacity (CC)",
        "type": "number",
        "step": "1",
        "min": "0",
        "help": "Engine displacement in cubic centimeters.",
    },
    "max_power": {
        "label": "Max Power (bhp)",
        "type": "number",
        "step": "0.1",
        "min": "0",
        "help": "Maximum power in bhp.",
    },
    "car_age": {
        "label": "Car Age (years)",
        "type": "number",
        "step": "1",
        "min": "0",
        "help": "Age used by the trained model.",
    },
}


SECTION_LAYOUT = [
    {
        "title": "Vehicle Identity",
        "fields": ["brand", "fuel", "seller_type", "transmission", "owner"],
    },
    {
        "title": "Usage and Condition",
        "fields": ["km_driven", "mileage", "engine", "max_power", "car_age"],
    },
]


def load_artifact():
    """Load the trained model and saved preprocessing objects from disk."""
    model_path = MODEL_PATH if MODEL_PATH.exists() else LEGACY_MODEL_PATH
    with model_path.open("rb") as handle:
        return pickle.load(handle)


def clean_numeric_series(series: pd.Series) -> pd.Series:
    """Convert values like '20 kmpl' or '1197 CC' into numbers."""
    cleaned = series.astype(str)
    cleaned = cleaned.str.replace(" kmpl", "", regex=False)
    cleaned = cleaned.str.replace(" km/kg", "", regex=False)
    cleaned = cleaned.str.replace(" CC", "", regex=False)
    cleaned = cleaned.str.replace(" bhp", "", regex=False)
    return pd.to_numeric(cleaned, errors="coerce")


artifact = load_artifact()
model = artifact["model"]
encoders = artifact["encoders"]
feature_order = artifact["feature_order"]
category_fields = list(encoders.keys())
option_map = {field: list(encoder.classes_) for field, encoder in encoders.items()}


def build_defaults() -> dict:
    """Generate sensible default values for the prediction form."""
    data = pd.read_csv(DATA_PATH)

    # The dataset does not store brand separately, so we derive it from name.
    if "name" in data.columns:
        data = data.copy()
        data["brand"] = data["name"].astype(str).apply(lambda value: value.split()[0])

    defaults = {
        "km_driven": int(data["km_driven"].median()),
        "mileage": round(clean_numeric_series(data["mileage"]).median(), 1),
        "engine": int(round(clean_numeric_series(data["engine"]).median())),
        "max_power": round(clean_numeric_series(data["max_power"]).median(), 1),
        "car_age": int(max(0, 2021 - int(data["year"].median()))),
    }

    for field in category_fields:
        mode_series = data[field].dropna().mode()
        if not mode_series.empty:
            defaults[field] = mode_series.iloc[0]
        else:
            defaults[field] = option_map[field][0]

    return defaults


def format_currency_inr(value: float) -> str:
    """Format a number in Indian currency style."""
    amount = int(round(value))
    sign = "-" if amount < 0 else ""
    digits = str(abs(amount))

    if len(digits) <= 3:
        return f"RS. {sign}{digits}"

    last_three = digits[-3:]
    remaining = digits[:-3]
    parts = []

    while len(remaining) > 2:
        parts.insert(0, remaining[-2:])
        remaining = remaining[:-2]

    if remaining:
        parts.insert(0, remaining)

    return f"RS. {sign}{','.join(parts + [last_three])}"


DEFAULT_VALUES = build_defaults()
app = Flask(__name__)


def wants_json_response() -> bool:
    """Check whether the client expects JSON instead of HTML."""
    return (
        request.is_json
        or request.headers.get("X-Requested-With") == "XMLHttpRequest"
        or "application/json" in request.headers.get("Accept", "")
    )


def parse_numeric_value(payload, field: str) -> float:
    """Validate and convert a numeric input from the form."""
    raw_value = str(payload.get(field, "")).strip()
    if raw_value == "":
        raise ValueError(f"{FIELD_META[field]['label']} is required.")

    try:
        value = float(raw_value)
    except ValueError as exc:
        raise ValueError(f"{FIELD_META[field]['label']} must be a valid number.") from exc

    if value < 0:
        raise ValueError(f"{FIELD_META[field]['label']} cannot be negative.")

    return value


def encode_categorical_value(payload, field: str) -> int:
    """Encode a selected category using the saved label encoder."""
    raw_value = str(payload.get(field, "")).strip()
    if raw_value == "":
        raise ValueError(f"{FIELD_META[field]['label']} is required.")

    encoder = encoders[field]
    if raw_value not in encoder.classes_:
        raise ValueError(f"{FIELD_META[field]['label']} has an unsupported value.")

    return int(encoder.transform([raw_value])[0])


def build_feature_frame(payload) -> tuple[pd.DataFrame, dict]:
    """Prepare input data in the exact format expected by the model."""
    processed = {}

    # Use the same feature order.
    for field in feature_order:
        if field in category_fields:
            processed[field] = encode_categorical_value(payload, field)
        else:
            processed[field] = parse_numeric_value(payload, field)

    feature_frame = pd.DataFrame(
        [[processed[field] for field in feature_order]],
        columns=feature_order,
    )
    return feature_frame, processed


@app.route("/")
def index():
    """Display the prediction form."""
    # Pass shared data to the template .
    return render_template(
        "index.html",
        field_meta=FIELD_META,
        sections=SECTION_LAYOUT,
        options=option_map,
        feature_order=feature_order,
        defaults=DEFAULT_VALUES,
        form_values=DEFAULT_VALUES,
        result=None,
        error=None,
    )


@app.route("/predict", methods=["POST"])
def predict():
    """Receive user input, make a prediction, and return the result."""
    payload = request.get_json(silent=True) if request.is_json else request.form
    payload = payload or {}

    try:
        # Build a model-ready row  saved model generate the price.
        feature_frame, submitted_values = build_feature_frame(payload)
        prediction = float(model.predict(feature_frame)[0])
    except ValueError as exc:
        error_message = str(exc)
        if wants_json_response():
            return jsonify(success=False, error=error_message), 400
        return render_template(
            "index.html",
            field_meta=FIELD_META,
            sections=SECTION_LAYOUT,
            options=option_map,
            feature_order=feature_order,
            defaults=DEFAULT_VALUES,
            form_values=payload,
            result=None,
            error=error_message,
        ), 400

    result = {
        "predicted_price": prediction,
        "formatted_price": format_currency_inr(prediction),
        "submitted_values": submitted_values,
    }

    if wants_json_response():
        return jsonify(success=True, **result)

    return render_template(
        "index.html",
        field_meta=FIELD_META,
        sections=SECTION_LAYOUT,
        options=option_map,
        feature_order=feature_order,
        defaults=DEFAULT_VALUES,
        form_values=payload,
        result=result,
        error=None,
    )


if __name__ == "__main__":
    # Start the Flask development server for local testing.
    app.run(debug=True)
