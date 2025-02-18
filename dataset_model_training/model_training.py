import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report

# Load the dataset
inputDF = pd.read_csv("dataset_model_training/CBSE_Students_Dataset.csv")

# Encode categorical columns
learningLabelEncoder = LabelEncoder()
inputDF["LearningStyle"] = learningLabelEncoder.fit_transform(
    inputDF["LearningStyle"])
careerLabelEncoder = LabelEncoder()
inputDF["CareerInterest"] = careerLabelEncoder.fit_transform(
    inputDF["CareerInterest"])

# One-hot encode hobbies
hobbies = ["Sports", "Arts", "Music", "Dance",
           "Reading", "Technology", "Writing"]
for hobby in hobbies:
    inputDF[hobby] = inputDF["Hobbies"].apply(lambda x: 1 if hobby in x else 0)

# Prepare features and target
features = ["Age", "Grade", "LearningStyle", "Mathematics", "Science", "English",
            "Social Science", "Hindi"] + hobbies

# Reshape the data using melt
reshapedDF = pd.melt(
    inputDF,
    id_vars=["StudentID", "Name", "Age", "Grade",
             "CareerInterest"],  # Keep CareerInterest
    value_vars=["Mathematics", "Science", "English",
                "Social Science", "Hindi"],  # Subject columns
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

# Reordering columns using loc
XTrain = XTrain.loc[:, features]
# Train Random Forest model
rfModel = RandomForestClassifier(n_estimators=100, random_state=42)
rfModel.fit(XTrain, yTrain)

# Reordering columns using loc
XTest = XTest.loc[:, features]
# Evaluate the model
yPred = rfModel.predict(XTest)
print("Career Prediction Accuracy:", accuracy_score(yTest, yPred))
print(classification_report(yTest, yPred))

# Save the trained model
modelPath = "model/career_model.pkl"
joblib.dump(rfModel, modelPath)
print(f"Model saved to {modelPath}")

# Save the fitted LabelEncoder
joblib.dump(learningLabelEncoder, "model/learning_label_encoder.pkl")
print("LearningLabelEncoder saved to model/learning_label_encoder.pkl")

joblib.dump(careerLabelEncoder, "model/career_label_encoder.pkl")
print("CareerLabelEncoder saved to model/career_label_encoder.pkl")
