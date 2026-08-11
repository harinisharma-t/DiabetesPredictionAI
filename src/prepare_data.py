import pandas as pd
from sklearn.model_selection import train_test_split


def load_and_prepare_data():

    # Load dataset
    df = pd.read_csv("data/raw/diabetes.csv")

    # Features
    X = df.drop("Outcome", axis=1)

    # Target
    y = df["Outcome"]

    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    return X_train, X_test, y_train, y_test


if __name__ == "__main__":

    X_train, X_test, y_train, y_test = load_and_prepare_data()

    print("Features:")
    print(X_train.head())

    print("\nTraining Data Shape:", X_train.shape)
    print("Testing Data Shape:", X_test.shape)