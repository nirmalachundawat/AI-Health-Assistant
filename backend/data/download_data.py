# backend/data/download_data.py

import urllib.request
import os

URL = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"

COLUMNS = [
    "Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
    "Insulin", "BMI", "DiabetesPedigreeFunction", "Age", "Outcome"
]

def download():
    os.makedirs("backend/data", exist_ok=True)
    dest = "backend/data/diabetes.csv"

    if os.path.exists(dest):
        print("Dataset already exists, skipping download.")
        return

    print("Downloading PIMA Diabetes dataset...")
    urllib.request.urlretrieve(URL, dest)

    # Add headers
    with open(dest, "r") as f:
        content = f.read()
    with open(dest, "w") as f:
        f.write(",".join(COLUMNS) + "\n" + content)

    print(f"Dataset saved to {dest}")

if __name__ == "__main__":
    download()