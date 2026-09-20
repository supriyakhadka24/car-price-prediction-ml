from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from car_price_prediction import app


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
