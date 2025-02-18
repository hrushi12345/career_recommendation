import joblib
import pandas as pd
from flask import Flask, render_template, request
import urllib
import pymysql
pymysql.install_as_MySQLdb()
from models import db
from tableManagement import TableManagementClass as TMC

app = Flask(__name__)

DATABASE_PASSWORD_UPDATED = urllib.parse.quote_plus('Pass@1234')
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root:{
    DATABASE_PASSWORD_UPDATED}@localhost/education_path_planner'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

# Load the trained model and other dependencies
loadedModel = joblib.load("model/career_model.pkl")
learningLabelEncoder = joblib.load("model/learning_label_encoder.pkl")
careerLabelEncoder = joblib.load("model/career_label_encoder.pkl")

# Predefined mappings
hobbies = ["Sports", "Arts", "Music", "Dance",
           "Reading", "Technology", "Writing"]
features = ["Age", "Grade", "LearningStyle", "Mathematics", "Science", "English",
            "Social Science", "Hindi"] + hobbies
careerToSubjects = {
    "Engineer": ["Mathematics", "Science", "English"],
    "Doctor": ["Science", "English"],
    "Teacher": ["English", "Social Science", "Hindi"],
    "Scientist": ["Mathematics", "Science"],
    "Artist": ["English", "Hindi"],
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
    name = request.form["name"]
    gender = request.form["gender"]
    grade = request.form["grade"]
    learningStyle = request.form["learningStyle"]
    mathematics = int(request.form["mathematics"])
    science = int(request.form["science"])
    english = int(request.form["english"])
    socialScience = int(request.form["socialScience"])
    hindi = int(request.form["hindi"])
    careerInterest = request.form["careerInterest"]
    favSubjects = request.form.getlist("favSubjects")  # List of selected subjects
    userHobbies = request.form.getlist("hobbies")  # List of selected hobbies

    # Preprocess the data
    learningStyleEncoded = learningLabelEncoder.transform([learningStyle])[0]
    hobbyFeatures = {hobby: (1 if hobby in userHobbies else 0)
                     for hobby in hobbies}
    userData = {
        "Age": age,
        "Name": name,
        "Gender": gender,
        "Grade": grade,
        "LearningStyle": learningStyleEncoded,
        "Mathematics": mathematics,
        "Science": science,
        "English": english,
        "Social Science": socialScience,
        "Hindi": hindi,
        "CareerInterest": careerInterest,
        # **favSubjects,
        **hobbyFeatures
    }

    # Convert to DataFrame
    userDf = pd.DataFrame([userData], columns=features)

    # Predict career
    predictedCareerIndex = loadedModel.predict(userDf)[0]
    predictedCareer = careerLabelEncoder.inverse_transform(
        [predictedCareerIndex])[0]
    recommendedSubjects = careerToSubjects.get(predictedCareer, [])

    # Store inputData in database
    dataStoredMessage = TMC().dataAdditionInTables(
        request.form, predictedCareer, recommendedSubjects)

    # Render the result page
    return render_template(
        "result.html",
        career=predictedCareer,
        recommendedSubjects=recommendedSubjects
    )


if __name__ == "__main__":
    app.run(debug=True)
