import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import joblib
import os

# 8 Features: Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DPF, Age
X = np.array([
    [6, 148, 72, 35, 0, 33.6, 0.627, 50],
    [1, 85, 66, 29, 0, 26.6, 0.351, 31],
    [8, 183, 64, 0, 0, 23.3, 0.672, 32],
    [1, 89, 66, 23, 94, 28.1, 0.167, 21],
    [0, 137, 40, 35, 168, 43.1, 2.288, 33]
])
y = np.array([1, 0, 1, 0, 1])  # 1 = Diabetic, 0 = Non-Diabetic

# Create a pipeline that scales data then applies the classifier
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('clf', RandomForestClassifier(random_state=42))
])

pipeline.fit(X, y)

# Ensure the model directory exists and save the model
os.makedirs('model', exist_ok=True)
joblib.dump(pipeline, 'model/diabetes_model.pkl')
print("Model saved successfully to model/diabetes_model.pkl")