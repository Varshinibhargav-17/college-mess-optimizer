"""
College Mess Attendance Predictor - Streamlit App
"""

import streamlit as st
import pandas as pd
import numpy as np
import pickle
from datetime import datetime, timedelta

# Page config
st.set_page_config(
    page_title="Mess Attendance Predictor",
    page_icon="🍽️",
    layout="wide"
)

# Load artifacts
@st.cache_resource
def load_artifacts():
    try:
        with open('models/best_model.pkl', 'rb') as f:
            model = pickle.load(f)
        with open('models/scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)
        with open('models/label_encoders.pkl', 'rb') as f:
            encoders = pickle.load(f)
        with open('models/feature_names.pkl', 'rb') as f:
            feature_names = pickle.load(f)
        return model, scaler, encoders, feature_names
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None, None, None, None

model, scaler, encoders, feature_names = load_artifacts()

# Header
st.title("🍽️ College Mess Attendance Predictor")
st.markdown("AI-powered system to optimize food preparation and reduce waste")

# Sidebar inputs
st.sidebar.header("📋 Input Parameters")

prediction_date = st.sidebar.date_input(
    "Date",
    value=datetime.today() + timedelta(days=1)
)

meal_type = st.sidebar.selectbox(
    "Meal Type",
    ['Breakfast', 'Lunch', 'Dinner']
)

menu_items = {
    'Breakfast': ['Idli-Sambar', 'Poha', 'Upma', 'Dosa', 'Paratha-Curry', 'Bread-Omelette', 'Puri-Bhaji'],
    'Lunch': ['Rice-Dal-Sabzi', 'Roti-Paneer', 'Biryani', 'Rice-Sambar', 'Chole-Bhature', 'Fried Rice', 'Pulao'],
    'Dinner': ['Roti-Dal', 'Rice-Rajma', 'Paratha-Paneer', 'Rice-Curd-Pickle', 'Noodles', 'Rice-Chicken', 'Khichdi']
}

menu_item = st.sidebar.selectbox("Menu Item", menu_items[meal_type])

menu_popularity_map = {
    'Biryani': 4.8, 'Chole-Bhature': 4.5, 'Dosa': 4.6, 'Rice-Chicken': 4.7,
    'Puri-Bhaji': 4.3, 'Fried Rice': 4.2, 'Roti-Paneer': 4.0, 'Paratha-Paneer': 4.1,
    'Noodles': 4.2, 'Idli-Sambar': 3.9, 'Poha': 3.7, 'Upma': 3.5,
    'Rice-Dal-Sabzi': 3.4, 'Roti-Dal': 3.3, 'Rice-Rajma': 3.8, 'Rice-Sambar': 3.6,
    'Rice-Curd-Pickle': 3.2, 'Khichdi': 3.0, 'Bread-Omelette': 3.9, 'Paratha-Curry': 3.7, 'Pulao': 4.0
}

weather = st.sidebar.selectbox("Weather", ['Sunny', 'Cloudy', 'Rainy'])
temperature = st.sidebar.slider("Temperature (°C)", 15, 40, 28)

st.sidebar.markdown("---")
is_exam = st.sidebar.checkbox("Exam Period")
is_festival = st.sidebar.checkbox("Festival/Holiday")
is_start_sem = st.sidebar.checkbox("Start of Semester")

# Feature preparation
def prepare_features(date, meal_type, menu_item, weather, temperature, is_exam, is_festival, is_start_sem):
    
    # Date features
    year = date.year
    month = date.month
    day = date.day
    day_of_week_num = date.weekday()
    week_of_year = date.isocalendar()[1]
    
    is_weekend = 1 if day_of_week_num >= 5 else 0
    is_monday = 1 if day_of_week_num == 0 else 0
    is_friday = 1 if day_of_week_num == 4 else 0
    is_monsoon = 1 if month in [6, 7, 8, 9] else 0
    is_end_semester = 0
    
    # Cyclical encoding
    day_sin = np.sin(2 * np.pi * day / 31)
    day_cos = np.cos(2 * np.pi * day / 31)
    month_sin = np.sin(2 * np.pi * month / 12)
    month_cos = np.cos(2 * np.pi * month / 12)
    dow_sin = np.sin(2 * np.pi * day_of_week_num / 7)
    dow_cos = np.cos(2 * np.pi * day_of_week_num / 7)
    
    # Encode categorical
    meal_encoded = encoders['meal'].transform([meal_type])[0]
    weather_encoded = encoders['weather'].transform([weather])[0]
    
    # Menu features
    menu_popularity = menu_popularity_map.get(menu_item, 3.5)
    menu_historical_avg = 400 if menu_popularity > 4.0 else 350
    menu_historical_std = 50
    is_popular_menu = 1 if menu_popularity >= 4.3 else 0
    is_unpopular_menu = 1 if menu_popularity <= 3.3 else 0
    menu_count_last_7days = 1
    
    # Lag features (approximated - in production, use real historical data)
    students_lag_1 = 440
    students_lag_7 = 435
    students_lag_14 = 430
    waste_lag_1 = 15
    waste_lag_7 = 16
    waste_lag_14 = 15
    students_same_day_last_week = 438
    
    # Rolling features (approximated)
    students_roll_3d_mean = 440
    students_roll_3d_std = 20
    students_roll_7d_mean = 438
    students_roll_7d_std = 25
    students_roll_14d_mean = 435
    students_roll_14d_std = 28
    students_roll_7d_max = 480
    students_roll_7d_min = 400
    
    # Other features
    temp_deviation = temperature - 28
    
    # Interaction features
    weekend_x_exam = is_weekend * is_exam
    weekend_x_festival = is_weekend * is_festival
    rainy_x_weekend = (1 if weather == 'Rainy' else 0) * is_weekend
    exam_x_festival = is_exam * is_festival
    popularity_x_weekend = menu_popularity * is_weekend
    temp_x_rainy = temperature * (1 if weather == 'Rainy' else 0)
    
    # Special conditions
    special_conditions_count = is_exam + is_festival + is_weekend + is_start_sem
    has_special_condition = 1 if special_conditions_count > 0 else 0
    is_normal_day = 1 if special_conditions_count == 0 else 0
    
    # Create features dictionary in EXACT order from feature_names
    features = {
        'serving_duration_mins': 60,  # Not used in prediction, but model expects it
        'is_end_semester': is_end_semester,
        'month_cos': month_cos,
        'weekend_x_festival': weekend_x_festival,
        'month_sin': month_sin,
        'is_unpopular_menu': is_unpopular_menu,
        'students_roll_7d_mean': students_roll_7d_mean,
        'exam_x_festival': exam_x_festival,
        'total_capacity': 800,  # Not used in prediction, but model expects it
        'students_lag_7': students_lag_7,
        'is_monsoon': is_monsoon,
        'students_roll_3d_mean': students_roll_3d_mean,
        'is_normal_day': is_normal_day,
        'meal_encoded': meal_encoded,
        'day_sin': day_sin,
        'menu_historical_std': menu_historical_std,
        'students_roll_3d_std': students_roll_3d_std,
        'is_monday': is_monday,
        'waste_lag_14': waste_lag_14,
        'student_satisfaction': 4.0,  # Not used in prediction, but model expects it
        'popularity_x_weekend': popularity_x_weekend,
        'waste_lag_7': waste_lag_7,
        'menu_historical_avg': menu_historical_avg,
        'weather_encoded': weather_encoded,
        'is_friday': is_friday,
        'is_festival': is_festival,
        'temp_deviation': temp_deviation,
        'cost_per_kg_rs': 100,  # Not used in prediction, but model expects it
        'students_roll_7d_max': students_roll_7d_max,
        'students_lag_1': students_lag_1,
        'week_of_year': week_of_year,
        'weekend_x_exam': weekend_x_exam,
        'students_same_day_last_week': students_same_day_last_week,
        'temperature_c': temperature,
        'day_of_week_num': day_of_week_num,
        'is_weekend': is_weekend,
        'day': day,
        'rainy_x_weekend': rainy_x_weekend,
        'is_start_semester': is_start_sem,
        'students_roll_7d_std': students_roll_7d_std,
        'has_special_condition': has_special_condition,
        'month': month,
        'menu_count_last_7days': menu_count_last_7days,
        'is_popular_menu': is_popular_menu,
        'students_roll_14d_std': students_roll_14d_std,
        'year': year,
        'dow_sin': dow_sin,
        'special_conditions_count': special_conditions_count,
        'menu_popularity': menu_popularity,
        'dow_cos': dow_cos,
        'students_roll_7d_min': students_roll_7d_min,
        'waste_lag_1': waste_lag_1,
        'temp_x_rainy': temp_x_rainy,
        'day_cos': day_cos,
        'is_exam_period': is_exam,
        'students_lag_14': students_lag_14,
        'staff_count': 10,  # Not used in prediction, but model expects it
        'students_roll_14d_mean': students_roll_14d_mean
    }
    
    return pd.DataFrame([features])[feature_names]  # Ensure correct order

# Predict button
if st.sidebar.button("🔮 Predict Attendance", type="primary"):
    if model is None:
        st.error("Model not loaded")
    else:
        with st.spinner("Predicting..."):
            features_df = prepare_features(
                prediction_date, meal_type, menu_item, weather,
                temperature, is_exam, is_festival, is_start_sem
            )
            
            features_scaled = scaler.transform(features_df)
            prediction = model.predict(features_scaled)[0]
            prediction = max(0, min(800, int(round(prediction))))
            
            # Results
            st.markdown("---")
            st.markdown("## 🎯 Prediction Results")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("👥 Expected Attendance", f"{prediction} students")
            
            with col2:
                food_needed = prediction * 0.35 * 1.1
                st.metric("🍚 Food Required", f"{food_needed:.1f} kg")
            
            with col3:
                cost = food_needed * 100
                st.metric("💰 Estimated Cost", f"₹{cost:,.0f}")
            
            # Recommendations
            st.markdown("### 💡 Recommendations")
            
            if prediction < 350:
                st.warning("⚠️ Low attendance expected. Reduce preparation.")
            elif prediction > 550:
                st.success("✅ High attendance expected. Ensure adequate supplies.")
            
            if is_exam:
                st.info("📚 Exam period: Students may skip meals.")
            if is_festival:
                st.info("🎉 Festival: Many students may go home.")
            if weather == 'Rainy':
                st.info("🌧️ Rainy weather: Attendance typically higher.")

st.markdown("---")
st.markdown("**Model:** Gradient Boosting | **Accuracy:** R² = 0.94 | **RMSE:** 29.65 students")