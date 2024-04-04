# Compact Code Works Large Group Project

## Team members
The members of the team are:
- Mohammed (Miqdaad) Al-Hassan
- MD (Rahat) Hussain
- Ibrahim Ahmed
- Mohammed (Sameen) Ahmed
- Javed Hussain
- Adil Kassam
- Mohammed (Minhaj) Sajjad Rahman
- Liban Scekei

## Project structure
The project is called `journaling_app`.  It currently consists of a single app `journal`.

## Deployed version of the application
The deployed version of the application can be found at [https://mmalhassan.pythonanywhere.com/](https://mmalhassan.pythonanywhere.com/).

## Installation instructions
To install the software and use it in your local development environment, you must first set up and activate a local development environment.  From the root of the project:

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

Run Celery and Celery beat each on a separate terminal/bash:

```
$ celery -A journaling_app worker 
$ celery -A journaling_app beat
```

Run all tests with:
```
$ python3 manage.py test
```

*The above instructions should work in your version of the application.  If there are deviations, declare those here in bold.  Otherwise, remove this line.*

## Sources
The packages used by this application are specified in `requirements.txt`

## Usage of Generative AI

```
We generally used AI to help debug our code.

The only functionality generative AI was used for was for Celery which
was used to help send reminders to each user.
```
