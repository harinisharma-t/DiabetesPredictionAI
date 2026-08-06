from flask import Flask, render_template, request, Response
import pickle
import os
import csv
from io import BytesIO
from datetime import datetime

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from db import (
    create_database,
    save_prediction,
    get_all_predictions,
    get_statistics,
    search_predictions,
    export_predictions
)

app = Flask(__name__)

# Store the latest prediction for PDF generation
latest_prediction = {}

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

    total, high_risk, low_risk = get_statistics()

    return render_template(
        "index.html",
        total=total,
        high_risk=high_risk,
        low_risk=low_risk
    )


@app.route("/predict", methods=["POST"])
def predict():

    global latest_prediction

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

    save_prediction(
        features,
        result,
        confidence
    )

    # Save latest prediction for PDF
    latest_prediction = {
        "prediction": result,
        "confidence": confidence,
        "date": datetime.now().strftime("%d-%m-%Y %H:%M")
    }

    return render_template(
        "result.html",
        prediction=result,
        color=color,
        confidence=confidence
    )


@app.route("/history")
def history():

    search = request.args.get("search", "").strip()

    if search:
        predictions = search_predictions(search)
    else:
        predictions = get_all_predictions()

    return render_template(
        "history.html",
        predictions=predictions,
        search=search
    )


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/export")
def export():

    predictions = export_predictions()

    def generate():

        yield "ID,Glucose,BMI,Prediction,Confidence,Created At\n"

        for row in predictions:
            yield f"{row[0]},{row[2]},{row[6]},{row[9]},{row[10]},{row[11]}\n"

    return Response(
        generate(),
        mimetype="text/csv",
        headers={
            "Content-Disposition":
            "attachment; filename=prediction_history.csv"
        }
    )


@app.route("/download-pdf")
def download_pdf():

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=letter)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "Diabetes Prediction Report",
            styles["Title"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Prediction:</b> {latest_prediction.get('prediction', 'N/A')}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Confidence:</b> {latest_prediction.get('confidence', 'N/A')}%",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Date:</b> {latest_prediction.get('date', 'N/A')}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            "<br/><b>Disclaimer:</b> This report is generated using a "
            "Machine Learning model and is intended for educational "
            "purposes only. It is not a medical diagnosis.",
            styles["BodyText"]
        )
    )

    doc.build(story)

    pdf = buffer.getvalue()
    buffer.close()

    return Response(
        pdf,
        mimetype="application/pdf",
        headers={
            "Content-Disposition":
            "attachment; filename=Diabetes_Report.pdf"
        }
    )


if __name__ == "__main__":
    app.run(debug=True)