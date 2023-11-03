
---

# Habit Tracker App

The **Habit Tracker App** is a web application built with Django, providing users with a platform to set, track, and analyze their daily and weekly habits. Users can define their habits, specify the frequency (daily or weekly), set goals, and monitor their progress over time. The app offers insights into streaks, achievements, and missed completions, empowering users to cultivate positive habits and improve their productivity.

## Features

- **User Authentication**: Users can create accounts, log in, and log out to access the habit tracking features.
  
- **Habit Creation and Tracking**: Users can define their habits, set their periodicity (daily or weekly), and track their completion status.

- **Streaks and Achievements**: The app keeps track of users' streaks (consecutive completions) and displays achievements for reaching goals.

- **Insightful Analytics**: Users can view their longest streak, most missed habits, and analyze their habits' completion patterns.


## Usage

1. **Authentication**:
    - Create an account or log in if you already have one.

2. **Creating Habits**:
    - Define habits and set their periodicity and frequency (daily or weekly).

3. **Tracking Habits**:
    - Mark habits as completed each day or week.

4. **Viewing Analytics**:
    - Check streaks, achievements, and analyze habit completion trends.

## Installation

1. Clone the repository:
    ```
    git clone <repository-url>
    cd habit-tracker-app
    ```

2. Install the necessary dependencies:
    ```
     python -m venv venv
     window -> source venv/scripts/activate
     linux -> source venv/bin/activate
     pip install -r requirements.txt
    ```

3. Run the development server:
    ```
    python manage.py runserver
    ```
4. Run the tests:
    ```
     python manage.py test
     ```
5. Access the application at [http://localhost:8000](http://localhost:8000).

## Technologies Used

- Django: Web framework for building the application.
- HTML, CSS, JavaScript: Frontend design and interactivity.

