import pandas as pd
from sklearn.model_selection import train_test_split

# Load dataset
df = pd.read_csv("data/raw/diabetes.csv")

# Features (Input)
X = df.drop("Outcome", axis=1)

# Target (Output)
y = df["Outcome"]

print("Features:")
print(X.head())

print("\nTarget:")
print(y.head())

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("\nTraining Data Shape:", X_train.shape)
print("Testing Data Shape:", X_test.shape)