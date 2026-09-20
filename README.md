# Car Price Prediction System

A Machine Learning-based web application that predicts the estimated selling price of a used car based on its features.

The project uses **Linear Regression** and **Random Forest Regression** to analyse historical used-car data. Both models are evaluated using **MAE, RMSE, and R² Score**, and **Random Forest Regression is selected as the final model** based on its better overall performance.

The final model is integrated with a **Flask web application**, allowing users to enter car details and receive an estimated selling price. The application currently runs locally for the semester project.

---

##  Project Overview

The main purpose of this project is to estimate the selling price of a used car using Machine Learning.

The system takes information such as the car's brand, age, kilometres driven, fuel type, transmission, mileage, engine, and maximum power as input.

```text
Car Details
     ↓
Data Preprocessing
     ↓
Machine Learning Models
     ↓
Model Evaluation
     ↓
Random Forest Selected
     ↓
Flask Web Application
     ↓
Predicted Car Price


## Technologies Used

Python – Programming language
Pandas & NumPy – Data processing
Scikit-learn – Machine Learning
Matplotlib & Seaborn – Data visualization
Flask – Web application
HTML & CSS – User interface
Jupyter Notebook – Model development
Git & GitHub – Version control


Machine Learning Models

Two regression models were developed and compared:

Linear Regression

Used as the baseline model to establish a simple prediction benchmark.

Random Forest Regression

Used to capture more complex relationships between vehicle features and selling prices.

After comparing both models using R² Score, MAE, and RMSE, Random Forest Regression was selected as the final model because it provided better overall performance.


Input Features

The model uses the following vehicle features:

Car Brand
Kilometres Driven
Fuel Type
Seller Type
Transmission
Owner Type
Mileage
Engine
Maximum Power
Car Age

Categorical features are converted into numerical values during preprocessing using encoders.

## Project Workflow


Dataset
   ↓
Data Cleaning & Preprocessing
   ↓
Feature Engineering
   ↓
Train-Test Split
   ↓
Linear Regression
   ↓
Random Forest Regression
   ↓
Model Evaluation & Comparison
   ↓
Random Forest Selected
   ↓
Save Trained Model
   ↓
Flask Web Application
   ↓
Price Prediction


Model Evaluation

The models are evaluated using three standard regression metrics:

Metric	Description	Better Result
MAE	Average prediction error	Lower
RMSE	Measures prediction error with greater weight on large errors	Lower
R² Score	Measures how well the model explains price variation	Higher

## Project Structure
```text
car_price_prediction_ml/
├── app.py                         # Local development launcher
├── requirements.txt               # Runtime dependencies
├── requirements-dev.txt           # Local test dependencies
├── .python-version
├── data/
│   └── raw/Cardetails.csv         # Source dataset
├── models/
│   └── car_price_model.pkl        # Trained model artifact
├── notebooks/
│   └── Car_Price_Prediction.ipynb # Experimentation and training work
├── src/
│   └── car_price_prediction/
│       ├── __init__.py
│       ├── app.py                 # Flask application factory and routes
│       ├── config.py              # Project paths and feature definitions
│       ├── static/style.css
│       └── templates/index.html
└── tests/
   └── test_app.py
```

## Local Setup

Create and activate a virtual environment, then install the dependencies:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
```

Start the local Flask application from the project root:

```powershell
python app.py
```

Open `http://127.0.0.1:5000` in a browser. The application is intentionally configured for local development only; no Render, Gunicorn, or hosted deployment configuration is included at this stage.

Run the tests with:

```powershell
python -m pytest
```



## Main Files

`src/car_price_prediction/app.py` contains the Flask application and prediction logic. `models/car_price_model.pkl` stores the trained Random Forest model and preprocessing information. The notebook contains data analysis, preprocessing, model training, and evaluation.


👥 Team Members
Supriya Khadka
Neha Thapa Magar
Prashant Shrestha
Sandesh Khadka

Disclaimer

The predicted price is an estimated value based on historical used-car data. It may differ from the actual market price due to factors such as vehicle condition, location, market demand, maintenance history, and other factors.

⭐ If you find this project useful, please consider giving the repository a star!


