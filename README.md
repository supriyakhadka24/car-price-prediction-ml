#  Car Price Prediction System

A Machine Learning-based web application that predicts the estimated selling price of a used car based on its features.

The project uses **Linear Regression** and **Random Forest Regression** to analyse historical used-car data. Both models are evaluated using **MAE, RMSE, and R² Score**, and **Random Forest Regression is selected as the final model** based on its better overall performance.

The final model is integrated with a **Flask web application**, allowing users to enter car details and receive an estimated selling price.

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


 Technologies Used

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

Project Workflow


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

Project Structure
Car_Price_Prediction_Linear_Regression/
│
├── app.py
├── car_price_model.pkl
├── requirements.txt
├── .python-version
│
├── templates/
│   └── index.html
│
├── static/
│   └── style.css
│
└── Car_Price_Prediction_Linear_Regression.ipynb



Main Files

app.py – Flask application and prediction logic
car_price_model.pkl – Saved final Random Forest model and preprocessing information
index.html – Web application interface
style.css – Website styling
requirements.txt – Required Python packages
Car_Price_Prediction_Linear_Regression.ipynb – Data analysis, preprocessing, model training, and evaluation



⚙️ How to Run the Project

The following steps can be used to run the project locally.

1. Clone the Repository

Open PowerShell or Command Prompt and run:

git clone https://github.com/SandeshKhadka77/car-price-prediction-ml.git

Then move into the project folder:

cd car-price-prediction-ml
2. Create a Virtual Environment

Create a Python virtual environment:

python -m venv .venv
3. Activate the Virtual Environment
Windows PowerShell
.venv\Scripts\Activate.ps1

If PowerShell does not allow script execution, run:

Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned

Then activate the environment again:

.venv\Scripts\Activate.ps1

After successful activation, the terminal should show:

(.venv)
4. Install Required Packages

Install all required Python libraries using:

pip install -r requirements.txt

The main packages used by the project include:

Flask
Pandas
NumPy
Scikit-learn
Matplotlib
Seaborn
5. Run the Flask Application

After installing the required packages, run:

python app.py

The Flask application will start locally.

You should see a local address similar to:

http://127.0.0.1:5000

Open this address in a web browser to use the application.



👥 Team Members
Supriya Khadka
Neha Thapa Magar
Prashant Shrestha
Sandesh Khadka

Disclaimer

The predicted price is an estimated value based on historical used-car data. It may differ from the actual market price due to factors such as vehicle condition, location, market demand, maintenance history, and other factors.

⭐ If you find this project useful, please consider giving the repository a star!


