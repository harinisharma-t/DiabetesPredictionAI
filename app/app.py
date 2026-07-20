from flask import Flask, render_template, request
import pickle
import os

app = Flask(__name__)

# Load the trained model
model_path = os.path.join(os.path.dirname(__file__), "..", "models", "diabetes_model.pkl")

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

    if prediction[0] == 1:
        result = "Diabetic"
    else:
        result = "Not Diabetic"

    return render_template("result.html", prediction=result)


if __name__ == "__main__":
    app.run(debug=True)