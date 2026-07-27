from flask import Flask, render_template, request
import pickle
import os
from db import create_database, save_prediction, get_all_predictions

app = Flask(__name__)

# Create the SQLite database (if it doesn't already exist)
create_database()

# Load the trained model
model_path = os.path.join(
    os.path.dirname(__file__),
    "..",
    "models",
    "diabetes_model.pkl"
)

with open(model_path, "rb") as file:
    model = pickle.load(file)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    features = [
        float(request.form["Pregnancies"]),
        float(request.form["Glucose"]),
        float(request.form["BloodPressure"]),
        float(request.form["SkinThickness"]),
        float(request.form["Insulin"]),
        float(request.form["BMI"]),
        float(request.form["DiabetesPedigreeFunction"]),
        float(request.form["Age"])
    ]

    prediction = model.predict([features])

    probability = model.predict_proba([features])
    confidence = round(max(probability[0]) * 100, 2)

    if prediction[0] == 1:
        result = "⚠️ High Risk of Diabetes"
        color = "#dc3545"
    else:
        result = "✅ Low Risk of Diabetes"
        color = "#198754"

    # Save prediction to SQLite database
    save_prediction(
        features,
        result,
        confidence
    )

    return render_template(
        "result.html",
        prediction=result,
        color=color,
        confidence=confidence
    )
@app.route("/history")
def history():

    predictions = get_all_predictions()

    return render_template(
        "history.html",
        predictions=predictions
    )

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)