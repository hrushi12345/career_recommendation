from models import db, Student, Profile, Marks


class TableManagementClass:
    def dataAdditionInTables(self, inputData, predictedCareer, recommendedSubjects):
        age = int(inputData["age"])
        name = inputData["name"]
        gender = inputData["gender"]
        grade = inputData["grade"]
        learningStyle = inputData["learningStyle"]
        mathematics = int(inputData["mathematics"])
        science = int(inputData["science"])
        english = int(inputData["english"])
        socialScience = int(inputData["socialScience"])
        hindi = int(inputData["hindi"])
        careerInterest = inputData["careerInterest"]
        favSubjects = inputData.getlist(
            "favSubjects")  # List of selected subjects
        userHobbies = inputData.getlist("hobbies")  # List of selected hobbies

        # Step 1: Create Student entry
        student = Student(age=age, name=name, gender=gender, std=grade)
        db.session.add(student)
        db.session.commit()  # Commit to generate student ID

        # Step 2: Create Profile entry
        profile = Profile(
            st_id=student.id,
            overall_percentage=self.calculateOverallPercentage(
                [mathematics, science, english, socialScience, hindi]),
            type_of_learner=learningStyle,
            hobbies=userHobbies,
            favorite_subjects=favSubjects,
            recommended_subjects=recommendedSubjects,
            carrier_interest=careerInterest,
            predicted_career=predictedCareer
        )
        db.session.add(profile)

        # Step 3: Create Marks entries
        subjects = {
            'math': mathematics,
            'science': science,
            'english': english,
            'socialScience': socialScience,
            'hindi': hindi
        }

        for subject, score in subjects.items():
            mark = Marks(st_id=student.id, subject=subject, score=score)
            db.session.add(mark)

        db.session.commit()  # Commit all changes to the database

        return "Data stored successfully!"

    def calculateOverallPercentage(self, marks):
        return sum(marks) / len(marks)  # Simple average calculation
