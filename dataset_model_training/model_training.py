import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report

# Load the dataset
inputDF = pd.read_csv("dataset_model_training/CBSE_Students_Dataset.csv")

# Encode categorical columns
labelEncoder = LabelEncoder()
inputDF["LearningStyle"] = labelEncoder.fit_transform(inputDF["LearningStyle"])
inputDF["CareerInterest"] = labelEncoder.fit_transform(inputDF["CareerInterest"])

# One-hot encode hobbies
hobbies = ["Sports", "Arts", "Music", "Dance",
           "Reading", "Technology", "Writing"]
for hobby in hobbies:
    inputDF[hobby] = inputDF["Hobbies"].apply(lambda x: 1 if hobby in x else 0)

# Prepare features and target
features = ["Age", "Grade", "LearningStyle", "Mathematics", "Science", "English",
            "SocialStudies", "Hindi"] + hobbies

# Reshape the data using melt
reshapedDF = pd.melt(
    inputDF,
    id_vars=["StudentID", "Name", "Age", "Grade",
             "CareerInterest"],  # Keep CareerInterest
    value_vars=["Mathematics", "Science", "English", "Hindi",
                "Sanskrit", "SocialStudies"],  # Subject columns
    var_name="Subject",
    value_name="TestScore"
)

# Pivot the table to prepare for training
X = reshapedDF.pivot_table(
    index="StudentID", columns="Subject", values="TestScore", fill_value=0)
X.reset_index(inplace=True)

# Retrieve CareerInterest as the target variable
y = inputDF.set_index("StudentID")["CareerInterest"]

# Merge additional features
X = X.merge(inputDF[["StudentID"] + hobbies +
            ["Age", "Grade", "LearningStyle"]], on="StudentID")

# Split the dataset
XTrain, XTest, yTrain, yTest = train_test_split(
    X.drop(columns=["StudentID"]), y, test_size=0.2, random_state=42)

# Train Random Forest model
rfModel = RandomForestClassifier(n_estimators=100, random_state=42)
rfModel.fit(XTrain, yTrain)

# Evaluate the model
yPred = rfModel.predict(XTest)
print("Career Prediction Accuracy:", accuracy_score(yTest, yPred))
print(classification_report(yTest, yPred))

# Save the trained model
modelPath = "model/career_model.pkl"
joblib.dump(rfModel, modelPath)
print(f"Model saved to {modelPath}")


# # Reverse encoding for career interest
# decoded_career = {index: career for career, index in enumerate(labelEncoder.classes_)}

# # Map careers to recommended subjects
# career_to_subjects = {
#     "Engineer": ["Mathematics", "Science", "English"],
#     "Doctor": ["Science", "Biology", "English"],
#     "Teacher": ["English", "SocialStudies", "Hindi"],
#     "Scientist": ["Mathematics", "Science", "SocialStudies"],
#     "Artist": ["Arts", "English", "Hindi"],
#     "Entrepreneur": ["Mathematics", "SocialStudies", "English"],
#     "Government Services": ["SocialStudies", "English", "Hindi"],
# }

# # Reverse encoding for career interest
# decoded_career = {index: career for index, career in enumerate(labelEncoder.classes_)}

# # Recommend subjects based on career prediction
# for student_index, career_index in enumerate(yPred[:10]):  # Example: First 10 students
#     career = decoded_career[int(career_index)]  # Ensure proper mapping with integer type
#     recommended_subjects = career_to_subjects.get(career, [])
#     print(f"Student {student_index + 1}: Career - {career}, Recommended Subjects - {recommended_subjects}")
