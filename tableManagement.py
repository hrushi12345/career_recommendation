from models import db, Student, Profile, Marks


class TableManagementClass:
    def dataAdditionInTables(self, inputData, predictedCareer, recommendedSubjects, id):
        age = int(inputData["age"])
        gender = inputData["gender"]
        grade = inputData["grade"]
        learningStyle = inputData["learningStyle"]
        mathematics = int(inputData["mathematics"])
        science = int(inputData["science"])
        english = int(inputData["english"])
        socialScience = int(inputData["socialScience"])
        hindi = int(inputData["hindi"])
        careerInterest = inputData["careerInterest"]
        userHobbies = inputData.getlist("hobbies")  # List of selected hobbies
        strength = inputData.getlist("strength")
        weekness = inputData.getlist("weekness")

        # Step 1: Create Student entry
        student = Student.query.filter_by(id=id).first()

        # Step 2: Create Profile entry
        profile = Profile(
            st_id=student.id,
            gender = gender,
            std = grade,
            age = age,
            overall_percentage=self.calculateOverallPercentage(
                [mathematics, science, english, socialScience, hindi]),
            type_of_learner=learningStyle,
            hobbies=userHobbies,
            recommended_subjects=recommendedSubjects,
            carrier_interest=careerInterest,
            predicted_career=predictedCareer,
            strength = strength,
            weekness = weekness
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
