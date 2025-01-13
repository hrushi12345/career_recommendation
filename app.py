from flask import Flask, render_template, request
import joblib
import pandas as pd

app = Flask(__name__)

# Load the trained model and other dependencies
loaded_model = joblib.load("model/career_model.pkl")
learning_label_encoder = joblib.load("model/learning_label_encoder.pkl")
career_label_encoder = joblib.load("model/career_label_encoder.pkl")

# Predefined mappings
hobbies = ["Sports", "Arts", "Music", "Dance", "Reading", "Technology", "Writing"]
features = ["Age", "Grade", "LearningStyle", "Mathematics", "Science", "English", 
            "Social Science", "Hindi"] + hobbies
career_to_subjects = {
    "Engineer": ["Mathematics", "Science", "English"],
    "Doctor": ["Science", "Biology", "English"],
    "Teacher": ["English", "Social Science", "Hindi"],
    "Scientist": ["Mathematics", "Science", "Social Science"],
    "Artist": ["Arts", "English", "Hindi"],
    "Entrepreneur": ["Mathematics", "Social Science", "English"],
    "Government Services": ["Social Science", "English", "Hindi"],
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    # Get form data
    age = int(request.form["age"])
    grade = request.form["grade"]
    learning_style = request.form["learningStyle"]
    mathematics = int(request.form["mathematics"])
    science = int(request.form["science"])
    english = int(request.form["english"])
    social_science = int(request.form["socialScience"])
    hindi = int(request.form["hindi"])
    user_hobbies = request.form.getlist("hobbies")  # List of selected hobbies

    # Preprocess the data
    learning_style_encoded = learning_label_encoder.transform([learning_style])[0]
    hobby_features = {hobby: (1 if hobby in user_hobbies else 0) for hobby in hobbies}
    user_data = {
        "Age": age,
        "Grade": grade,
        "LearningStyle": learning_style_encoded,
        "Mathematics": mathematics,
        "Science": science,
        "English": english,
        "Social Science": social_science,
        "Hindi": hindi,
        **hobby_features
    }

    # Convert to DataFrame
    user_df = pd.DataFrame([user_data], columns=features)

    # Predict career
    predicted_career_index = loaded_model.predict(user_df)[0]
    predicted_career = career_label_encoder.inverse_transform([predicted_career_index])[0]
    recommended_subjects = career_to_subjects.get(predicted_career, [])

    # Render the result page
    return render_template(
        "result.html", 
        career=predicted_career, 
        recommended_subjects=recommended_subjects
    )

if __name__ == "__main__":
    app.run(debug=True)
