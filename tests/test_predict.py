import pickle


def test_prediction():

    # Load trained model
    with open("models/diabetes_model.pkl", "rb") as file:
        model = pickle.load(file)

    # Sample patient data
    sample = [[6, 148, 72, 35, 0, 33.6, 0.627, 50]]

    # Make prediction
    prediction = model.predict(sample)

    # Prediction should contain exactly one result
    assert len(prediction) == 1

    # Prediction should be either 0 or 1
    assert prediction[0] in [0, 1]