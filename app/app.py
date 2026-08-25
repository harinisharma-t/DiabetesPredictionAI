from flask import Flask, render_template, request, redirect
import pickle
import os
import csv
import logging
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
    export_predictions,
    clear_predictions
)

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
# Store the latest prediction for PDF generation
latest_prediction = {}


# Create the SQLite database
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


# ---------------------------------------------------------
# HOME PAGE
# ---------------------------------------------------------

@app.route("/")
def home():

    total, high_risk, low_risk = get_statistics()

    return render_template(
        "index.html",
        total=total,
        high_risk=high_risk,
        low_risk=low_risk
    )


# ---------------------------------------------------------
# PREDICTION
# ---------------------------------------------------------

@app.route("/predict", methods=["POST"])
def predict():

    global latest_prediction

    # -----------------------------------------
    # STEP 1: Check whether values are numeric
    # -----------------------------------------

    try:

        pregnancies = float(request.form["Pregnancies"])
        glucose = float(request.form["Glucose"])
        blood_pressure = float(request.form["BloodPressure"])
        skin_thickness = float(request.form["SkinThickness"])
        insulin = float(request.form["Insulin"])
        bmi = float(request.form["BMI"])

        diabetes_pedigree = float(
            request.form["DiabetesPedigreeFunction"]
        )

        age = float(request.form["Age"])

    except (ValueError, TypeError, KeyError):

        return jsonify({
            "success": False,
            "error": "Please enter valid numeric values for all fields."
        }), 400


    # -----------------------------------------
    # STEP 2: Validate ranges
    # -----------------------------------------

    if pregnancies < 0:

        return jsonify({
            "success": False,
            "error": "Pregnancies cannot be negative."
        }), 400


    if glucose < 0 or glucose > 300:

        return jsonify({
            "success": False,
            "error": "Glucose must be between 0 and 300."
        }), 400


    if blood_pressure < 0 or blood_pressure > 200:

        return jsonify({
            "success": False,
            "error": "Blood Pressure must be between 0 and 200."
        }), 400


    if skin_thickness < 0 or skin_thickness > 100:

        return jsonify({
            "success": False,
            "error": "Skin Thickness must be between 0 and 100."
        }), 400


    if insulin < 0 or insulin > 900:

        return jsonify({
            "success": False,
            "error": "Insulin must be between 0 and 900."
        }), 400


    if bmi < 10 or bmi > 70:

        return jsonify({
            "success": False,
            "error": "BMI must be between 10 and 70."
        }), 400


    if diabetes_pedigree < 0 or diabetes_pedigree > 3:

        return jsonify({
            "success": False,
            "error": "Diabetes Pedigree Function must be between 0 and 3."
        }), 400


    if age < 1 or age > 120:

        return jsonify({
            "success": False,
            "error": "Age must be between 1 and 120."
        }), 400


    # -----------------------------------------
    # STEP 3: Prepare features
    # -----------------------------------------

    features = [
        pregnancies,
        glucose,
        blood_pressure,
        skin_thickness,
        insulin,
        bmi,
        diabetes_pedigree,
        age
    ]


    # -----------------------------------------
    # STEP 4: Make prediction
    # -----------------------------------------

    prediction = model.predict([features])

    probability = model.predict_proba([features])

    confidence = round(
        max(probability[0]) * 100,
        2
    )


    # -----------------------------------------
    # STEP 5: Generate result
    # -----------------------------------------

    if prediction[0] == 1:

        result = "⚠️ High Risk of Diabetes"
        color = "#dc3545"

    else:

        result = "✅ Low Risk of Diabetes"
        color = "#198754"


    # -----------------------------------------
    # STEP 6: Save prediction to database
    # -----------------------------------------

    save_prediction(
        features,
        result,
        confidence
    )


    # -----------------------------------------
    # STEP 7: Save latest prediction for PDF
    # -----------------------------------------

    latest_prediction = {

        "prediction": result,

        "confidence": confidence,

        "date": datetime.now().strftime(
            "%d-%m-%Y %H:%M"
        )
    }


    # -----------------------------------------
    # STEP 8: Show result page
    # -----------------------------------------

    return render_template(
        "result.html",
        prediction=result,
        color=color,
        confidence=confidence
    )


# ---------------------------------------------------------
# PREDICTION HISTORY
# ---------------------------------------------------------

@app.route("/history")
def history():

    search = request.args.get(
        "search",
        ""
    ).strip()


    if search:

        predictions = search_predictions(search)

    else:

        predictions = get_all_predictions()


    return render_template(
        "history.html",
        predictions=predictions,
        search=search
    )

@app.route("/clear-history", methods=["POST"])
def clear_history():

    clear_predictions()

    return redirect("/history")


# ---------------------------------------------------------
# ABOUT PAGE
# ---------------------------------------------------------

@app.route("/about")
def about():

    return render_template(
        "about.html"
    )


# ---------------------------------------------------------
# EXPORT CSV
# ---------------------------------------------------------

@app.route("/export")
def export():

    predictions = export_predictions()


    def generate():

        yield "ID,Glucose,BMI,Prediction,Confidence,Created At\n"

        for row in predictions:

            yield (
                f"{row[0]},"
                f"{row[2]},"
                f"{row[6]},"
                f"{row[9]},"
                f"{row[10]},"
                f"{row[11]}\n"
            )


    return Response(

        generate(),

        mimetype="text/csv",

        headers={
            "Content-Disposition":
            "attachment; filename=prediction_history.csv"
        }
    )


# ---------------------------------------------------------
# DOWNLOAD PDF REPORT
# ---------------------------------------------------------

@app.route("/download-pdf")
def download_pdf():

    buffer = BytesIO()


    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter
    )


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
            f"<b>Prediction:</b> "
            f"{latest_prediction.get('prediction', 'N/A')}",
            styles["BodyText"]
        )
    )


    story.append(
        Paragraph(
            f"<b>Confidence:</b> "
            f"{latest_prediction.get('confidence', 'N/A')}%",
            styles["BodyText"]
        )
    )


    story.append(
        Paragraph(
            f"<b>Date:</b> "
            f"{latest_prediction.get('date', 'N/A')}",
            styles["BodyText"]
        )
    )


    story.append(
        Paragraph(
            "<br/><b>Disclaimer:</b> "
            "This report is generated using a Machine Learning model "
            "and is intended for educational purposes only. "
            "It is not a medical diagnosis. "
            "Please consult a healthcare professional.",
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


# ---------------------------------------------------------
# RUN APPLICATION
# ---------------------------------------------------------

if __name__ == "__main__":
    logger.info("Diabetes Prediction AI application started.")
    app.run(debug=True)