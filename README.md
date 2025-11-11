# Student Performance Tracker

A Django web application for tracking and visualizing student performance data.

## Features

- Upload student performance data via CSV files
- Interactive dashboard with visualizations using Plotly
- Track student scores, attendance, and performance by subject
- Admin interface for data management

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

3. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

4. Run the development server:
```bash
python manage.py runserver
```

5. Access the application at `http://127.0.0.1:8000/`

## CSV Format

Upload CSV files with the following columns:
- student: Student name
- subject: Subject name
- score: Numeric score
- attendance: Attendance percentage
- term: Academic term
- date_recorded: Date in YYYY-MM-DD format

## Project Structure

- `tracker/` - Main application
  - `models.py` - Student and Performance models
  - `views.py` - Dashboard and upload views
  - `forms.py` - File upload form
  - `templates/` - HTML templates
- `performance_project/` - Django project settings
- `uploads/` - Uploaded CSV files storage
