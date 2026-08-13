# Diabetes Prediction AI

A Machine Learning-based web application that predicts the risk of diabetes from patient health measurements.

The project combines a trained Machine Learning model with a Flask web application, SQLite database, input validation, prediction history, CSV export, and PDF report generation.

> **Disclaimer:** This project is intended for educational purposes only and is not a medical diagnostic tool.

---

## Problem Statement

Diabetes is a common chronic disease that can be difficult to identify early without appropriate screening.

The goal of this project is to build a Machine Learning system that can analyze common patient health measurements and estimate whether the patient is at a higher or lower risk of diabetes.

The prediction is presented through a simple web interface so that the complete Machine Learning workflow can be demonstrated in an accessible way.

---

## Dataset

The project uses the **Pima Indians Diabetes Dataset**.

The model uses the following eight input features:

| Feature | Description |
|---|---|
| Pregnancies | Number of pregnancies |
| Glucose | Plasma glucose concentration |
| BloodPressure | Diastolic blood pressure |
| SkinThickness | Triceps skin fold thickness |
| Insulin | 2-Hour serum insulin |
| BMI | Body Mass Index |
| DiabetesPedigreeFunction | Diabetes pedigree function |
| Age | Age of the patient |

The target variable represents whether the patient has diabetes.

---

## Machine Learning Models

Several Machine Learning algorithms were explored and compared during development.

| Model | Purpose |
|---|---|
| Logistic Regression | Baseline model |
| Decision Tree | Tree-based comparison |
| Random Forest | Ensemble tree model |
| XGBoost / Gradient Boosting | Boosting-based model |
| Support Vector Machine | Distance/margin-based model |

The final application uses the selected trained model saved as a serialized model file.

The purpose of comparing multiple models was to avoid choosing a model based only on intuition and instead evaluate their performance using appropriate classification metrics.

---

## Evaluation Metrics

The models were evaluated using:

- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC

For a diabetes screening problem, recall is particularly important because missing a patient who may be at risk can be more concerning than incorrectly flagging a low-risk patient.

---

## Application Architecture

```text
                    ┌─────────────────────┐
                    │     User / Browser   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     Flask App       │
                    │      app/app.py     │
                    └──────────┬──────────┘
                               │
                  ┌────────────┴────────────┐
                  │                         │
                  ▼                         ▼
        ┌──────────────────┐      ┌──────────────────┐
        │ Input Validation │      │  SQLite Database │
        └────────┬─────────┘      │   diabetes.db   │
                 │                └──────────────────┘
                 ▼
        ┌──────────────────┐
        │ ML Model         │
        │ diabetes_model   │
        │      .pkl        │
        └────────┬─────────┘
                 │
                 ▼
        ┌──────────────────┐
        │ Prediction Result│
        │ + Confidence     │
        └──────────────────┘