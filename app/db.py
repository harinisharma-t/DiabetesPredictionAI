import sqlite3
import os

DATABASE_NAME = os.path.join(
    os.path.dirname(__file__),
    "diabetes.db"
)


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def create_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pregnancies REAL,
            glucose REAL,
            blood_pressure REAL,
            skin_thickness REAL,
            insulin REAL,
            bmi REAL,
            diabetes_pedigree REAL,
            age REAL,
            prediction TEXT,
            confidence REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()

    print("Database created successfully.")


def save_prediction(features, prediction, confidence):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO predictions (
            pregnancies,
            glucose,
            blood_pressure,
            skin_thickness,
            insulin,
            bmi,
            diabetes_pedigree,
            age,
            prediction,
            confidence
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        features[0],
        features[1],
        features[2],
        features[3],
        features[4],
        features[5],
        features[6],
        features[7],
        prediction,
        confidence
    ))

    connection.commit()
    connection.close()


def get_all_predictions():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM predictions
        ORDER BY created_at DESC
    """)

    data = cursor.fetchall()

    connection.close()

    return data


def get_statistics():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM predictions")
    total = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM predictions WHERE prediction = ?",
        ("⚠️ High Risk of Diabetes",)
    )
    high_risk = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM predictions WHERE prediction = ?",
        ("✅ Low Risk of Diabetes",)
    )
    low_risk = cursor.fetchone()[0]

    connection.close()

    return (total, high_risk, low_risk)


def search_predictions(search_text):
    connection = get_connection()
    cursor = connection.cursor()

    search = f"%{search_text}%"

    cursor.execute("""
        SELECT *
        FROM predictions
        WHERE prediction LIKE ?
           OR CAST(glucose AS TEXT) LIKE ?
           OR CAST(age AS TEXT) LIKE ?
        ORDER BY created_at DESC
    """, (search, search, search))

    data = cursor.fetchall()

    connection.close()

    return data

def export_predictions():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM predictions
        ORDER BY created_at DESC
    """)

    data = cursor.fetchall()

    connection.close()

    return data
def clear_predictions():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM predictions")

    conn.commit()
    conn.close()