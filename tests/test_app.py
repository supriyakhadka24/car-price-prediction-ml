import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from car_price_prediction import create_app


def test_home_page_loads():
    client = create_app().test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"Car Price Prediction System" in response.data


def test_invalid_prediction_returns_bad_request():
    client = create_app().test_client()

    response = client.post("/predict", data={})

    assert response.status_code == 400


def test_get_predict_redirects_to_home():
    client = create_app().test_client()

    response = client.get("/predict")

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")


def test_prediction_preserves_submitted_values():
    client = create_app().test_client()

    response = client.post(
        "/predict",
        data={
            "brand": "Maruti",
            "fuel": "Petrol",
            "seller_type": "Individual",
            "transmission": "Manual",
            "owner": "First Owner",
            "km_driven": "45000",
            "mileage": "21.5",
            "engine": "1197",
            "max_power": "81",
            "car_age": "5",
        },
    )

    assert response.status_code == 200
    assert b'value="45000"' in response.data
    assert b'option value="Maruti" selected' in response.data
    assert b"Predicted Selling Price" in response.data
