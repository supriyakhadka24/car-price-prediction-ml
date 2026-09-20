from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = PROJECT_ROOT / "models" / "car_price_model.pkl"

CATEGORICAL_FIELDS = ["brand", "fuel", "seller_type", "transmission", "owner"]
NUMERIC_FIELDS = ["km_driven", "mileage", "engine", "max_power", "car_age"]

DEFAULT_FORM_VALUES = {
	"brand": "",
	"fuel": "",
	"seller_type": "",
	"transmission": "",
	"owner": "",
	"km_driven": "50000",
	"mileage": "22.5",
	"engine": "1248",
	"max_power": "74",
	"car_age": "6",
}
