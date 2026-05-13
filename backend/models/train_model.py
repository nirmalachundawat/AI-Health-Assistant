# backend/models/train_model.py

import sys
import os
sys.path.append(os.path.abspath("."))

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

from backend.data.preprocess import load_and_clean, split_features, scale_features

MODEL_PATH = "backend/models/diabetes_model.pkl"

def train():
    print("=== Training Diabetes Prediction Model ===\n")

    # Load and clean data
    df = load_and_clean()
    X, y = split_features(df)

    # Split into train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"\nTrain size: {X_train.shape[0]}, Test size: {X_test.shape[0]}")

    # Scale features
    X_train_scaled, X_test_scaled = scale_features(X_train, X_test)

    # Train Random Forest
    print("\nTraining Random Forest Classifier...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=6,
        random_state=42,
        class_weight="balanced"
    )
    model.fit(X_train_scaled, y_train)

    # Evaluate
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nModel Accuracy: {accuracy * 100:.2f}%")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=["No Diabetes", "Diabetes"]))

    # Save model
    os.makedirs("backend/models", exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"\nModel saved to {MODEL_PATH}")

if __name__ == "__main__":
    train()