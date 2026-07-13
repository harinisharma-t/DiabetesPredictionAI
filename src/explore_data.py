import pandas as pd

# Load the dataset
df = pd.read_csv("data/raw/diabetes.csv")

# Display first 5 rows
print("========== First 5 Rows ==========")
print(df.head())

# Dataset information
print("\n========== Dataset Information ==========")
df.info()

# Summary statistics
print("\n========== Summary Statistics ==========")
print(df.describe())

# Missing values
print("\n========== Missing Values ==========")
print(df.isnull().sum())

# Target column
print("\n========== Outcome Count ==========")
print(df["Outcome"].value_counts())