# Career Recommendation System

## Project Description

The Career Recommendation System helps 8th to 10th grade students get personalized career suggestions based on their interests, hobbies, academic performance, and favorite subjects. The model uses data collected from students, including their age, subjects with marks, favorite subjects, career interests, and hobbies.

The web application is built using Flask, and it allows students to input their information via a user-friendly form. Based on this input, the system recommends suitable career options and provides a suggestion for subjects to pursue for further studies.

### Features:
- **User Input Form**: Students can enter their name, age, subjects with marks, favorite subjects, career interests, and hobbies.
- **Career Recommendation**: The system recommends careers based on the user inputs.
- **Subject Recommendation**: The system suggests relevant subjects to be taken up for further studies.
- **Database Integration**: Data is stored in MySQL, using tables such as `student`, `profile`, and `marks` to manage the students' information and recommendations.

## Tech Stack
- **Flask**: Web framework to handle requests and render HTML templates.
- **MySQL**: Database to store and retrieve students' data.
- **Jinja2**: Templating engine used for rendering HTML in Flask.
- **Python**: The primary language used for developing the backend logic.
- **HTML/CSS**: For designing the user input form and the front-end interface.

## Setup Instructions

### Prerequisites

Make sure you have the following installed:
- **Python 3.12.3**  
- **MySQL Server**

#### [Python 3.12 Setup Steps](https://www.python.org/downloads/release/python-3123/)
- Follow the link for the installation steps and make sure to add Python to your system's PATH during installation.

#### [MySQL Setup Steps](https://dev.mysql.com/doc/refman/8.0/en/installing.html)
- Follow the link to set up MySQL server on your system.

### Create Python Virtual Environment and Install Flask

1. Open the command line in the project folder.
   
2. To create a virtual environment:
   ```bash
   python -m venv env
   ```

3. To activate the environment:
   - On Windows:
     ```bash
     env\Scripts\activate
     ```

4. Install the required Python packages:
   ```bash
   pip install -r req.txt
   ```

### Setup Database in MySQL

1. Open **MySQL Workbench** by searching it in the Windows application tray.

2. In the **Menu bar**, click on **Database**.

3. Click **Connect to Database** and then click **OK**.

4. In the **Schemas** panel (middle left), you will see the list of databases.

5. Below **View (Menu bar)**, click the **+** button to create a new schema.

6. Enter your required database name and click the **Apply** button at the bottom right.

7. The created schema should now appear in the left pane. Right-click on it and select **Set as Default Schema**.

### Update Database Credentials

1. Open `config.json` file in your project folder.

2. Update the database credentials in the `config.json` with the following information:
   ```json
   {
       "username": "your-mysql-username",
       "password": "your-mysql-password",
       "host": "localhost",
       "database": "career_recommendation"
   }
   ```

### Create Database Tables

1. In the project folder, activate the Python virtual environment by running:
   ```bash
   env\Scripts\activate
   ```

2. Run the `create_tables.py` script to create the necessary tables in your database:
   ```bash
   python create_tables.py
   ```

### Running the Project

Once the above steps are completed, run the Flask application:

1. In the project folder, make sure the environment is activated.

2. Run the application using:
   ```bash
   python app.py
   ```

3. Open your browser and go to `http://127.0.0.1:5000` to access the Career Recommendation form.

## Usage

1. Enter the required details such as Name, Age, Subjects with Marks, Favorite Subjects, Career Interests, and Hobbies.
2. After submitting the form, the system will recommend suitable career options based on the provided data.
3. The recommendations will also suggest subjects that the student should focus on for further studies.

## Future Enhancements

- Improve the recommendation model with more accurate machine learning algorithms.
- Add a feature for students to save their recommendations and track their progress over time.
- Extend the user interface with additional features such as career paths, salary insights, and skills required for recommended careers.

## Contributing

Feel free to fork the repository, submit issues, and open pull requests with any improvements or features you would like to contribute!

## License

This project is licensed under the MIT License.

## Acknowledgments

- Flask Documentation: https://flask.palletsprojects.com/
- MySQL Documentation: https://dev.mysql.com/doc/

