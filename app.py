import joblib
import json
import urllib
import uuid
import pandas as pd
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for, session, flash
import pymysql
pymysql.install_as_MySQLdb()
from models import db, Student, Profile
from tableManagement import TableManagementClass as TMC

app = Flask(__name__)
app.secret_key = "!@#$%QWER^&*()POIYTREWQ"

# Open and read the config file
with open('config.json', 'r') as file:
    data = json.load(file)
dbUserName = urllib.parse.quote_plus(data['username'])
dbPassword = urllib.parse.quote_plus(data['password'])
dbHost = data['host']
dbName = data['database']
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{dbUserName}:{dbPassword}@{dbHost}/{dbName}'
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

# Engineer, Doctor, Teacher, Scientist, Artist, Entrepreneur, Government Services
### 🔹 Default Page → Login
@app.route('/')
def home():
    return render_template('home.html')  # Home page


@app.route('/index')
def index():
    if 'id' not in session:
        return redirect(url_for('login'))  # Ensure user is logged in
    return render_template('index.html')

### 🔹 User Registration Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password)

        # Check if user already exists
        existing_user = Student.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered!", "danger")
            return redirect(url_for('register'))

        # Create user account
        # id = str(uuid.uuid4())
        user = Student(name=name, email=email, passwordHash=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash("Account created! Please login.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

### 🔹 User Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = Student.query.filter_by(email=email).first()
        if user and check_password_hash(user.passwordHash, password):
            session['id'] = user.id
            session['email'] = user.email
            flash("Login successful!", "success")
            return redirect(url_for('index'))
        else:
            flash("Invalid credentials!", "danger")

    return render_template('login.html')

### 🔹 Logout Route
@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully!", "info")
    return redirect(url_for('login'))

@app.route("/predict", methods=["POST"])
def predict():
    if 'id' not in session:
        return redirect(url_for('login'))  # Ensure user is logged in

    # Get form data
    age = int(request.form["age"])
    gender = request.form["gender"]
    grade = request.form["grade"].split("t")[0]
    learningStyle = request.form["learningStyle"]
    mathematics = int(request.form["mathematics"])
    science = int(request.form["science"])
    english = int(request.form["english"])
    socialScience = int(request.form["socialScience"])
    hindi = int(request.form["hindi"])
    careerInterest = request.form["careerInterest"]
    userHobbies = request.form.getlist("hobbies")  # List of selected hobbies

    # Preprocess the data
    learningStyleEncoded = learningLabelEncoder.transform([learningStyle])[0]
    hobbyFeatures = {hobby: (1 if hobby in userHobbies else 0)
                     for hobby in hobbies}
    
    name = Student.query.filter_by(id=session['id']).first().name
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
        request.form, predictedCareer, recommendedSubjects, session['id'])

    # Render the result page
    return render_template(
        "result.html",
        career=predictedCareer,
        recommendedSubjects=recommendedSubjects
    )


@app.route("/recommended_path", methods=["GET"])
def recommended_path():
    if 'id' not in session:
        return redirect(url_for('login'))  # Ensure user is logged in

    predictedCareer, recommendedSubjects = TMC().dataRetrievalFromTables(session['id'])

    # Render the result page
    return render_template(
        "result.html",
        career=predictedCareer,
        recommendedSubjects=recommendedSubjects
    )

if __name__ == "__main__":
    app.run(debug=True)
