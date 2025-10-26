
# 🍽️ College Mess Attendance Prediction Model

## Model Information
- **Model Type**: GradientBoostingRegressor
- **Training Date**: 2025-10-26
- **Version**: 1.0
- **Framework**: scikit-learn / XGBoost

## Performance Metrics
- **MAE**: 23.71 students
- **RMSE**: 29.98 students
- **R² Score**: 0.9399
- **MAPE**: 6.34%

## Training Data
- **Training Samples**: 681
- **Test Samples**: 171
- **Features**: 53
- **Date Range**: 2024-01-15 00:00:00 to 2024-10-24 00:00:00

## Model Purpose
Predicts student attendance in college mess to:
- Optimize food preparation quantities
- Reduce food waste
- Save costs
- Improve operational efficiency

## Key Features
Top 5 most important features:

50. students_roll_3d_mean (0.2220)
10. has_special_condition (0.1938)
6. menu_historical_avg (0.1397)
8. is_festival (0.0811)
45. menu_historical_std (0.0686)

## Business Impact
- **Monthly Savings**: ₹12,445.41
- **Yearly Savings**: ₹151,419.16
- **Waste Reduction**: 4.15 kg per meal
- **CO₂ Reduction**: 3.8 tonnes per year

## Usage
```python
import pickle
import pandas as pd

# Load model
with open('models/best_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Load scaler
with open('models/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

# Prepare input data
X_new = pd.DataFrame(...)  # Your features
X_scaled = scaler.transform(X_new)

# Predict
prediction = model.predict(X_scaled)
print(f"Expected attendance: {prediction[0]:.0f} students")
```

## Limitations
- Trained on synthetic data (requires validation with real data)
- Performance may vary during unprecedented events
- Requires periodic retraining with new data
- Limited to current menu items and patterns

## Maintenance
- **Retraining Frequency**: Monthly recommended
- **Monitoring**: Track MAE and RMSE in production
- **Updates**: Add new features as they become available

## Contact
- **Developer**: [Your Name]
- **Date**: 2025-10-26
- **GitHub**: [Your GitHub]
