# Diabetes Prediction API

## Overview

The Diabetes Prediction application provides a `/predict` endpoint
that accepts patient information and uses the trained Machine Learning
model to generate a diabetes risk prediction.

---

## Endpoint

### POST `/predict`

This endpoint receives patient information from the prediction form.

---

## Input Fields

The following fields are required:

| Field | Type | Description |
|---|---|---|
| Pregnancies | number | Number of pregnancies |
| Glucose | number | Blood glucose level |
| BloodPressure | number | Blood pressure |
| SkinThickness | number | Skin thickness measurement |
| Insulin | number | Insulin level |
| BMI | number | Body Mass Index |
| DiabetesPedigreeFunction | number | Diabetes pedigree function |
| Age | number | Patient age |

---

## Example Request

The Flask application currently receives the prediction data
through form data:

```text
Pregnancies=2
Glucose=120
BloodPressure=70
SkinThickness=20
Insulin=79
BMI=25.5
DiabetesPedigreeFunction=0.351
Age=35