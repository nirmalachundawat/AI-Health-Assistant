# backend/data/preprocess.py

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import joblib
import os

DATA_PATH = "backend/data/diabetes.csv"
SCALER_PATH = "backend/models/scaler.pkl"

# Columns where 0 is medically invalid — replace with median
ZERO_INVALID_COLS = ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]

def load_and_clean():
    df = pd.read_csv(DATA_PATH)
    print(f"Loaded dataset: {df.shape[0]} rows, {df.shape[1]} columns")

    # Replace invalid 0s with NaN then fill with median
    for col in ZERO_INVALID_COLS:
        df[col] = df[col].replace(0, np.nan)
        median_val = df[col].median()
        df[col] = df[col].fillna(median_val)
        print(f"  Fixed {col}: replaced 0s with median ({median_val:.2f})")

    return df

def split_features(df):
    X = df.drop("Outcome", axis=1)
    y = df["Outcome"]
    return X, y

def scale_features(X_train, X_test=None):
    os.makedirs("backend/models", exist_ok=True)
    scaler = StandardScaler()

    # Fit on numpy array to avoid feature name warnings at inference
    X_train_scaled = scaler.fit_transform(X_train.values)
    joblib.dump(scaler, SCALER_PATH)
    print(f"Scaler saved to {SCALER_PATH}")

    if X_test is not None:
        X_test_scaled = scaler.transform(X_test.values)
        return X_train_scaled, X_test_scaled

    return X_train_scaled

def get_feature_names():
    return [
        "Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
        "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"
    ]

if __name__ == "__main__":
    df = load_and_clean()
    print("\nSample data after cleaning:")
    print(df.head())
    print("\nOutcome distribution:")
    print(df["Outcome"].value_counts())