import pickle

# Load the saved model
with open("models/diabetes_model.pkl", "rb") as file:
    model = pickle.load(file)

print("Model loaded successfully!")

# Sample patient data
sample = [[6, 148, 72, 35, 0, 33.6, 0.627, 50]]

prediction = model.predict(sample)

if prediction[0] == 1:
    print("Prediction: Diabetic")
else:
    print("Prediction: Not Diabetic")