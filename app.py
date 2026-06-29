from flask import Flask, render_template, request
import joblib

model = joblib.load("model.pkl")

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    study_hours = float(request.form["study_hours"])
    attendance = float(request.form["attendance"])
    previous_marks = float(request.form["previous_marks"])
    sleep_hours = float(request.form["sleep_hours"])

    prediction = model.predict([[study_hours, attendance, previous_marks, sleep_hours]])
    predicted_marks = round(prediction[0], 2)

    suggestions = []

    if study_hours < 3:
        suggestions.append("Increase your study hours.")

    if attendance < 80:
        suggestions.append("Improve your attendance.")

    if sleep_hours < 6:
        suggestions.append("Sleep at least 7 hours.")

    if previous_marks < 60:
        suggestions.append("Revise basic concepts.")

    if predicted_marks >= 90:
        suggestions.append("Excellent! Keep up the good work.")

    return render_template(
    "index.html",
    prediction=prediction,
    suggestions=suggestions,
    study_hours=study_hours,
    attendance=attendance,
    previous_marks=previous_marks,
    sleep_hours=sleep_hours
)

if __name__ == "__main__":
    app.run(debug=True)