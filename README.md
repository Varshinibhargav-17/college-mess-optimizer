# College Mess Attendance Predictor

## 🍽️ Project Overview
The **College Mess Attendance Predictor** is an AI-powered system designed to predict daily student attendance in a college mess. Using historical attendance data, weather conditions, menu information, and special events, the system provides accurate predictions to optimize food preparation, reduce waste, and save costs.  

The application includes a **Gradient Boosting model**, pre-processing pipelines, and a **Streamlit-based interface** for real-time predictions and historical trend visualization.

---

## 🎯 Key Features
- Predict daily student attendance for Breakfast, Lunch, and Dinner.
- Incorporates weather, menu popularity, and special conditions (exam, festival, semester start).
- Generates recommended food quantities with buffer and estimated cost.
- Shows prediction confidence intervals based on model RMSE.
- Displays historical trends and averages by meal type and day of the week.
- Provides actionable recommendations for low/high attendance days.
- Ready for deployment as a web application using Streamlit.

---

## 📊 Data & Feature Engineering
- **Input Data:** Historical attendance records with meal type, menu, and environmental features.
- **Feature Engineering:**
  - Date-based features: day, month, day-of-week, week-of-year
  - Cyclical encodings for day, month, and day-of-week
  - Weather encoding and temperature deviation
  - Lag and rolling features for attendance and waste
  - Interaction features combining weekend, exam, festival, and weather effects
  - Special conditions and popularity indicators

- **Scaling:** All numeric features are scaled using `StandardScaler` for model input.

---

## 🧠 Model
- **Algorithm:** Gradient Boosting Regressor (best performing)
- **Training Data:** 681 samples, 58 features
- **Test Data:** 171 samples
- **Performance Metrics:**
  - Test MAE: 23.74 students
  - Test RMSE: 29.65 students
  - Test R²: 0.9412
  - Test MAPE: 6.32%

- **Business Impact:**
  - Potential monthly savings: ₹12,463
  - Potential yearly savings: ₹151,636
  - Waste reduction: 4.15 kg per meal
  - CO₂ reduction: 3.8 tonnes per year

- **Top Features:**  
  1. `students_roll_3d_mean`  
  2. `menu_historical_avg`  
  3. `special_conditions_count`  

---

## ⚡ Installation

1. Clone the repository:
```bash
git clone https://github.com/Varshinibhargav-17/college-mess-optimizer.git
cd college-mess-optimizer
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

---

## 🚀 Running the App

1. Ensure the following files exist in the `models/` folder:
   - `best_model.pkl`  
   - `scaler.pkl`  
   - `label_encoders.pkl`  
   - `feature_names.pkl`  

2. Run the Streamlit app:
```bash
streamlit run app.py
```

3. Open the URL shown in the terminal (usually `http://localhost:8501`) to interact with the app.

---


## 📦 Dependencies
Key Python packages used:
- `pandas`  
- `numpy`  
- `scikit-learn`  
- `xgboost`  
- `plotly`  
- `streamlit`  

Install via:
```bash
pip install pandas numpy scikit-learn xgboost plotly streamlit
```

---

## 🔧 Future Improvements
- Retrain model monthly with new attendance data.
- Implement ensemble methods for improved accuracy.
- Add automatic feature updates from live data.
- Integrate REST API deployment using FastAPI or Flask.
- Real-time dashboard for monitoring attendance predictions and waste reduction.
- Collect user feedback to refine predictions.

---

## ⚠️ Notes
- Ensure that **feature names** used for prediction match those used during model training to avoid errors.
- Model assumes approximate lag/rolling features if historical data is unavailable.
- Predictions are clamped between 0 and 800 students for valid attendance range.
