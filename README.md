# Compact Journal - 5CCS2SEG Large Group Project

## Project Overview
Compact Journals is a web-based journaling application designed to help users build a daily journaling habit, track multiple aspects of their lives, and improve productivity and well-being. Users can create multiple journals for different purposes, with each journal containing daily entries that function like “pages” in a book. The application also supports collaborative features through groups and friends, allowing shared journaling, accountability, and teamwork. The platform is fully responsive and can be accessed on desktops, tablets, and mobile devices. It was built using Django and Python for the backend, and HTML, CSS, and JavaScript for the frontend.

## Key Features
Users can create and manage their own accounts, view and update profiles, and personalize their journaling experience. Journals and daily entries can be created, edited, and deleted, with options for public or private visibility. Users can also import multimedia files into entries, use templates to streamline journaling, and export individual or group journals to PDF for offline viewing.

The application includes social and collaborative functionality: users can send friend requests, manage friendships, create and join groups, and collaborate on group journals. Group owners can manage members, create or delete group entries, and transfer ownership when leaving a group. Notifications keep users informed about activity in journals, friendships, and groups.

To encourage engagement, the app implements gamification features. Users earn points for actions like creating journals or entries, leveling up as they accumulate points, with safeguards to prevent point abuse. Daily reminders motivate users to maintain journaling habits, with notifications sent to prompt or congratulate users based on their progress.

## Team members
The members of the team Compact Code Works are:
- Mohammed Miqdaad Al-Hassan
- MD Rahat Hussain
- Ibrahim Ahmed
- Mohammed Sameen Ahmed
- Javed Hussain
- Adil Kassam
- Mohammed Minhaj Sajjad Rahman
- Liban Scekei

## Project Structure
The project is called `journaling_app` and currently consists of a single app, `journal`.  
Key directories and files:

- `journaling_app/` – Main Django project folder containing settings, URLs, and WSGI configuration.  
- `journal/` – Django app containing models, views, templates, tasks (Celery), and tests.  
- `templates/` – HTML templates used for rendering the pages.  
- `static/` – Static files (CSS, JavaScript, images) for the frontend.  
- `db.sqlite3` – SQLite database used for local development.  
- `requirements.txt` – List of Python dependencies required to run the project.  
- `manage.py` – Django management script for running server, migrations, tests, etc.  

> Note: Celery tasks and scheduled jobs are defined in `journal/tasks.py`. The production Celery configuration is in `settings.py` but commented out for local development.

## Original Deployment
The original deployed version of this application was hosted at [https://mmalhassan.pythonanywhere.com/](https://mmalhassan.pythonanywhere.com/), but it is no longer actively maintained or available.  
This repository contains the project for local development and testing purposes. To run the app locally, follow the instructions in the sections below.
> Note: For local development, Celery is configured to run synchronously so background tasks execute immediately without requiring Redis.


## Installation Instructions
To install the software and use it in your local development environment, first set up and activate a Python virtual environment. From the root of the project:
```
$ virtualenv venv
$ source venv/bin/activate
```
Install all required packages:
```
$ pip3 install -r requirements.txt
```
Migrate the database:
```
$ python3 manage.py migrate
```
Seed the development database with:
```
$ python3 manage.py seed
```
Run all tests with:
```
$ python3 manage.py test
```

## Running the Application Locally
Run the Django development server:
```
$ python3 manage.py runserver
```

## Celery (Background Tasks)
In this local development version, Celery is configured to run tasks synchronously (immediately) for ease of testing.  
You do NOT need to run `celery worker` or `celery beat` locally; the tasks will execute automatically.  

> Note: The original production-ready Celery configuration (using a Redis broker and separate worker/beat processes) is still present in the code, commented out. It can be restored when deploying the application.  
```
$ celery -A journaling_app worker 
$ celery -A journaling_app beat
```

## Sources
The packages used by this application are specified in `requirements.txt`

## Usage of Generative AI
```
We generally used AI to help debug our code.

The only functionality generative AI was used for was for Celery which
was used to help send reminders to each user.
```
