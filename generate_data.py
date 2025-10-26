"""
College Mess Data Generator
Creates realistic synthetic dataset for mess operations analysis
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# ============================================
# CONFIGURATION
# ============================================

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# College parameters
TOTAL_STUDENTS = 800
START_DATE = "2024-01-01"
END_DATE = "2024-10-24"

# Menu items
BREAKFAST_ITEMS = ['Idli-Sambar', 'Poha', 'Upma', 'Dosa', 'Paratha-Curry', 
                   'Bread-Omelette', 'Puri-Bhaji']
LUNCH_ITEMS = ['Rice-Dal-Sabzi', 'Roti-Paneer', 'Biryani', 'Rice-Sambar', 
               'Chole-Bhature', 'Fried Rice', 'Pulao']
DINNER_ITEMS = ['Roti-Dal', 'Rice-Rajma', 'Paratha-Paneer', 'Rice-Curd-Pickle', 
                'Noodles', 'Rice-Chicken', 'Khichdi']

# ============================================
# MENU SCHEDULER
# ============================================

class MenuScheduler:
    """Manages weekly menu rotation"""
    
    def __init__(self):
        self.weekly_menu = {
            'Monday': {
                'Breakfast': 'Idli-Sambar',
                'Lunch': 'Rice-Dal-Sabzi',
                'Dinner': 'Roti-Dal'
            },
            'Tuesday': {
                'Breakfast': 'Poha',
                'Lunch': 'Roti-Paneer',
                'Dinner': 'Rice-Rajma'
            },
            'Wednesday': {
                'Breakfast': 'Upma',
                'Lunch': 'Rice-Sambar',
                'Dinner': 'Paratha-Paneer'
            },
            'Thursday': {
                'Breakfast': 'Dosa',
                'Lunch': 'Biryani',
                'Dinner': 'Rice-Curd-Pickle'
            },
            'Friday': {
                'Breakfast': 'Paratha-Curry',
                'Lunch': 'Chole-Bhature',
                'Dinner': 'Noodles'
            },
            'Saturday': {
                'Breakfast': 'Bread-Omelette',
                'Lunch': 'Fried Rice',
                'Dinner': 'Roti-Paneer'
            },
            'Sunday': {
                'Breakfast': 'Puri-Bhaji',
                'Lunch': 'Rice-Chicken',
                'Dinner': 'Khichdi'
            }
        }
        
        # Menu popularity scores (1-5)
        self.popularity = {
            'Biryani': 4.8, 'Chole-Bhature': 4.5, 'Dosa': 4.6, 
            'Rice-Chicken': 4.7, 'Puri-Bhaji': 4.3, 'Fried Rice': 4.2,
            'Roti-Paneer': 4.0, 'Paratha-Paneer': 4.1, 'Noodles': 4.2,
            'Idli-Sambar': 3.9, 'Poha': 3.7, 'Upma': 3.5,
            'Rice-Dal-Sabzi': 3.4, 'Roti-Dal': 3.3, 'Rice-Rajma': 3.8,
            'Rice-Sambar': 3.6, 'Rice-Curd-Pickle': 3.2, 'Khichdi': 3.0,
            'Bread-Omelette': 3.9, 'Paratha-Curry': 3.7, 'Pulao': 4.0
        }
    
    def get_menu(self, day_name, meal_type):
        """Get menu for specific day and meal"""
        return self.weekly_menu[day_name][meal_type]
    
    def get_popularity(self, menu_item):
        """Get popularity score for menu item"""
        return self.popularity.get(menu_item, 3.5)

# ============================================
# DATA GENERATOR
# ============================================

def generate_college_mess_data():
    """Generate realistic college mess data"""
    
    print("🚀 Starting data generation...")
    
    # Initialize
    menu_scheduler = MenuScheduler()
    dates = pd.date_range(start=START_DATE, end=END_DATE, freq='D')
    data = []
    
    # Track menu repetition
    recent_menus = {'Breakfast': [], 'Lunch': [], 'Dinner': []}
    
    # Generate data for each day
    for idx, date in enumerate(dates):
        day_of_week = date.day_name()
        month = date.month
        day_num = date.day
        week_of_year = date.isocalendar()[1]
        
        # Special conditions
        is_exam = ((month == 5 and day_num > 15) or 
                   (month == 11 and day_num > 15) or 
                   (month == 12 and day_num < 20))
        
        is_festival = ((month == 8 and 13 <= day_num <= 17) or
                       (month == 10 and 20 <= day_num <= 26) or
                       (month == 3 and 6 <= day_num <= 10) or
                       (month == 1 and day_num == 26))
        
        is_start_sem = (month in [1, 8]) and (day_num <= 14)
        is_end_sem = ((month == 5 and day_num > 15) or 
                      (month == 11 and day_num > 15))
        is_weekend = day_of_week in ['Saturday', 'Sunday']
        
        # Weather
        is_monsoon = month in [6, 7, 8, 9]
        if is_monsoon:
            weather = random.choices(['Rainy', 'Cloudy', 'Sunny'], 
                                    weights=[0.5, 0.3, 0.2])[0]
        else:
            weather = random.choices(['Sunny', 'Cloudy', 'Rainy'], 
                                    weights=[0.6, 0.3, 0.1])[0]
        
        temperature = np.random.normal(28 if not is_monsoon else 24, 3)
        
        # Base attendance by day
        base_attendance_rate = {
            'Monday': 0.75, 'Tuesday': 0.78, 'Wednesday': 0.76,
            'Thursday': 0.74, 'Friday': 0.65, 'Saturday': 0.55, 
            'Sunday': 0.50
        }
        
        # Generate for each meal
        for meal_type in ['Breakfast', 'Lunch', 'Dinner']:
            
            # Get menu
            menu_item = menu_scheduler.get_menu(day_of_week, meal_type)
            popularity = menu_scheduler.get_popularity(menu_item)
            
            # Calculate attendance
            base_rate = base_attendance_rate[day_of_week]
            
            # Meal-specific rates
            meal_multiplier = {
                'Breakfast': 0.70,
                'Lunch': 0.85,
                'Dinner': 0.75
            }
            
            attendance_rate = base_rate * meal_multiplier[meal_type]
            
            # Adjustments
            if is_exam:
                attendance_rate *= 0.90
            if is_festival:
                attendance_rate *= 0.40
            if weather == 'Rainy':
                attendance_rate *= 1.10
            if is_start_sem:
                attendance_rate *= 0.95
            if is_end_sem:
                attendance_rate *= 0.85
            
            # Popularity boost
            popularity_boost = (popularity - 3.5) / 5  # Scale to -0.1 to 0.26
            attendance_rate *= (1 + popularity_boost)
            
            # Menu repetition check (fatigue)
            if menu_item in recent_menus[meal_type][-3:]:
                attendance_rate *= 0.92  # 8% drop for repetition
            
            # Cap attendance
            attendance_rate = min(attendance_rate, 0.95)
            
            # Calculate students
            expected_students = int(TOTAL_STUDENTS * attendance_rate)
            actual_students = max(0, int(np.random.normal(expected_students, 
                                                          expected_students * 0.08)))
            
            # Food calculations
            food_per_person_kg = 0.35  # 350 grams
            buffer_percentage = 1.10   # 10% extra
            
            food_prepared_kg = actual_students * food_per_person_kg * buffer_percentage
            
            # Consumption rate (not everyone finishes)
            consumption_rate = random.uniform(0.85, 0.95)
            food_consumed_kg = actual_students * food_per_person_kg * consumption_rate
            
            # Waste
            food_wasted_kg = food_prepared_kg - food_consumed_kg
            waste_percentage = (food_wasted_kg / food_prepared_kg * 100) if food_prepared_kg > 0 else 0
            
            # Costs
            cost_per_kg = random.uniform(80, 150)
            total_cost = food_prepared_kg * cost_per_kg
            waste_cost = food_wasted_kg * cost_per_kg
            
            # Additional features
            staff_count = random.randint(8, 12)
            serving_duration = random.randint(45, 90)
            
            # Student satisfaction (based on popularity + freshness)
            freshness_score = random.uniform(3.5, 5.0)
            satisfaction_score = (popularity * 0.7 + freshness_score * 0.3)
            
            # Append data
            data.append({
                'date': date,
                'year': date.year,
                'month': month,
                'day': day_num,
                'day_of_week': day_of_week,
                'week_of_year': week_of_year,
                'meal_type': meal_type,
                'menu_item': menu_item,
                'menu_popularity': popularity,
                'weather': weather,
                'temperature_c': round(temperature, 1),
                'is_exam_period': is_exam,
                'is_festival': is_festival,
                'is_weekend': is_weekend,
                'is_start_semester': is_start_sem,
                'is_end_semester': is_end_sem,
                'is_monsoon': is_monsoon,
                'total_capacity': TOTAL_STUDENTS,
                'students_attended': actual_students,
                'attendance_rate': round(attendance_rate * 100, 2),
                'food_prepared_kg': round(food_prepared_kg, 2),
                'food_consumed_kg': round(food_consumed_kg, 2),
                'food_wasted_kg': round(food_wasted_kg, 2),
                'waste_percentage': round(waste_percentage, 2),
                'cost_per_kg_rs': round(cost_per_kg, 2),
                'total_cost_rs': round(total_cost, 2),
                'waste_cost_rs': round(waste_cost, 2),
                'staff_count': staff_count,
                'serving_duration_mins': serving_duration,
                'student_satisfaction': round(satisfaction_score, 2)
            })
            
            # Update recent menus
            recent_menus[meal_type].append(menu_item)
            if len(recent_menus[meal_type]) > 7:
                recent_menus[meal_type].pop(0)
        
        # Progress indicator
        if (idx + 1) % 30 == 0:
            print(f"✓ Generated data for {idx + 1} days...")
    
    return pd.DataFrame(data)

# ============================================
# SAVE AND ANALYZE
# ============================================

def save_and_analyze_data(df):
    """Save dataset and print analysis"""
    
    # Create data directory if it doesn't exist
    os.makedirs('data/raw', exist_ok=True)
    
    # Save to CSV
    output_file = 'data/raw/college_mess_data.csv'
    df.to_csv(output_file, index=False)
    print(f"\n✅ Dataset saved to: {output_file}")
    
    # Print analysis
    print("\n" + "="*60)
    print("📊 DATASET SUMMARY")
    print("="*60)
    
    print(f"\n📅 Date Range: {df['date'].min()} to {df['date'].max()}")
    print(f"📋 Total Records: {len(df):,}")
    print(f"🍽️  Total Meals Served: {len(df):,}")
    print(f"📆 Number of Days: {df['date'].nunique()}")
    
    print("\n" + "-"*60)
    print("👥 ATTENDANCE STATISTICS")
    print("-"*60)
    print(f"Average Students per Meal: {df['students_attended'].mean():.0f}")
    print(f"Maximum Attendance: {df['students_attended'].max()}")
    print(f"Minimum Attendance: {df['students_attended'].min()}")
    print(f"Average Attendance Rate: {df['attendance_rate'].mean():.1f}%")
    
    print("\n" + "-"*60)
    print("🗑️  FOOD WASTE STATISTICS")
    print("-"*60)
    print(f"Total Food Prepared: {df['food_prepared_kg'].sum():,.2f} kg")
    print(f"Total Food Consumed: {df['food_consumed_kg'].sum():,.2f} kg")
    print(f"Total Food Wasted: {df['food_wasted_kg'].sum():,.2f} kg")
    print(f"Average Waste per Meal: {df['food_wasted_kg'].mean():.2f} kg")
    print(f"Average Waste Percentage: {df['waste_percentage'].mean():.1f}%")
    
    print("\n" + "-"*60)
    print("💰 COST ANALYSIS")
    print("-"*60)
    print(f"Total Cost: ₹{df['total_cost_rs'].sum():,.2f}")
    print(f"Total Waste Cost: ₹{df['waste_cost_rs'].sum():,.2f}")
    print(f"Average Daily Waste Cost: ₹{df.groupby('date')['waste_cost_rs'].sum().mean():,.2f}")
    print(f"Potential Monthly Savings: ₹{df.groupby('date')['waste_cost_rs'].sum().mean() * 30:,.2f}")
    
    print("\n" + "-"*60)
    print("⭐ MOST POPULAR MENU ITEMS")
    print("-"*60)
    popular_items = df.groupby('menu_item').agg({
        'students_attended': 'mean',
        'student_satisfaction': 'mean'
    }).sort_values('students_attended', ascending=False).head(5)
    
    for idx, (item, row) in enumerate(popular_items.iterrows(), 1):
        print(f"{idx}. {item}")
        print(f"   Avg Attendance: {row['students_attended']:.0f} students")
        print(f"   Satisfaction: {row['student_satisfaction']:.1f}/5.0")
    
    print("\n" + "-"*60)
    print("📉 HIGHEST WASTE ITEMS")
    print("-"*60)
    waste_items = df.groupby('menu_item')['food_wasted_kg'].mean().sort_values(ascending=False).head(5)
    
    for idx, (item, waste) in enumerate(waste_items.items(), 1):
        print(f"{idx}. {item}: {waste:.2f} kg average waste")
    
    print("\n" + "-"*60)
    print("📊 MEAL TYPE COMPARISON")
    print("-"*60)
    meal_comparison = df.groupby('meal_type').agg({
        'students_attended': 'mean',
        'food_wasted_kg': 'mean',
        'waste_cost_rs': 'mean'
    }).round(2)
    print(meal_comparison)
    
    print("\n" + "-"*60)
    print("📅 DAY-WISE ATTENDANCE PATTERN")
    print("-"*60)
    day_pattern = df.groupby('day_of_week')['attendance_rate'].mean().sort_values(ascending=False)
    for day, rate in day_pattern.items():
        print(f"{day}: {rate:.1f}%")
    
    print("\n" + "="*60)
    print("✅ DATA GENERATION COMPLETE!")
    print("="*60)
    
    return df

# ============================================
# MAIN EXECUTION
# ============================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🏫 COLLEGE MESS DATA GENERATOR")
    print("="*60 + "\n")
    
    # Generate data
    df = generate_college_mess_data()
    
    # Save and analyze
    df = save_and_analyze_data(df)
    
    print(f"\n📁 Next steps:")
    print(f"   1. Check the generated file: data/raw/college_mess_data.csv")
    print(f"   2. Open it in Excel or use pandas to explore")
    print(f"   3. Start building your ML models!")
    print("\n")