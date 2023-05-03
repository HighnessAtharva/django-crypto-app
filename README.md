# Django Crypto App - ASETT Project

Introducing the 3-part technical tutorial series on building a Django project that lets users manage their cryptocurrency portfolios. The app also offers a user registration system that enables users to create an account and build their own crypto portfolio with a password reset and referral system.

👉🏻 Follow along for a more guided learning:-  


[Tutorial Series Part 1](https://atharvashah.netlify.app/blog/django-crypto-app/part1/) 


[Tutorial Series Part 2](https://atharvashah.netlify.app/blog/django-crypto-app/part2/)  


[Tutorial Series Part 3](https://atharvashah.netlify.app/blog/django-crypto-app/part3/)


**TECHNOLOGIES USED:**

- Language: Python 3.10
- Framework: Django 4.0+
- Database: SQLite [Default]
- API USED: [CoinGecko](https://www.coingecko.com/en/api/documentation) - Public Version, No API Key. Rate Limit is 10-25 req/minute
- Frontend: Bootstrap 5.1.3
- Testing: Django Test Framework
- Test Coverage: 90%+
- Development Methodology: TDD (Test Driven Development)

## How I Set Up The Project

For instructions on how to run this project on YOUR PC, see below ↘️ [How To Run This Project](#how-to-run-this-project)  

>**All steps are for a Windows 10 machine.**
>I followed these steps to set up the project:

```py
# cd into the folder where you want to create the project
cd django-crypto-app

# create a virtualenv
python -m venv env 

# activate the virtualenv
env\Scripts\activate  

# install needed packages
pip install django
pip install requests
pip install coverage

# start the django project in the current folder
django-admin startproject crypto .

# create a django app
python manage.py startapp mainapp

# make migrations (i'm sticking to the default sqlite db for now)
python manage.py makemigrations

# perform migrations to populate the db
python manage.py migrate

# create a superuser, enter username, email and password to login to the admin panel
python manage.py createsuperuser

# start the server
python manage.py runserver

# Django will start the server on port 8000 so open the browser and go to http://localhost:8000/

# Visit http://localhost:8000/admin to login to the admin panel

# I generated requirements.txt using the following command
pip freeze > requirements.txt
```

## How To Run This Project

You need app password for your email account for emailing. To know more about how to get your app password, see this [link](https://support.google.com/accounts/answer/185833?hl=en)

```py

# clone the repo
git clone https://github.com/HighnessAtharva/django-crypto-app.git

# cd into the project folder
cd django-crypto-app

# create a virtualenv
python -m venv env

# activate the virtualenv
env\Scripts\activate

# install the needed packages
pip install -r requirements.txt

# make a .env file and add the following variables
# EMAIL_HOST_USER=<your-email-here>
# EMAIL_HOST_PASSWORD=<your-app-password-here>
# See .env-example for more info, structure it in the same way as the .env-example file

# make migrations
python manage.py makemigrations
python manage.py migrate

# delete existing database if necessary, overwrite and make your own migrations and users

# create a superuser to login to the admin panel
python manage.py createsuperuser

# start the server
python manage.py runserver

```

## Docker

```py

# Ensure you have Docker Desktop installed and running

# cd into the project folder

# build the image
docker-compose build

# run the container
docker-compose up

# visit http://localhost:8000/

# stop the container
docker-compose down
```

## Database Schema

![Database Schema](https://github.com/HighnessAtharva/django-crypto-app/blob/main/assets/DB-layout.png?raw=true)

## How to Run Tests

All tests are written in the `tests.py` file in the `mainapp` folder.

```py

# to run all tests
python manage.py test

# to run tests for a specific class
python manage.py test -k <class-name>

# start coverage
coverage run --source='.' --omit=mainapp\tests.py manage.py test mainapp

# generate coverage report
coverage html

# check the htmlcov folder and open the index.html file

```

#### Coverage Report

![Coverage Report](https://github.com/HighnessAtharva/django-crypto-app/blob/main/assets/coverage.png?raw=true)

## Folder Structure and Important Files

`crypto` - The main project folder. Contains the `settings.py` file and the `urls.py` file.

`crypto\static` - Contains the static files for the project such as css, js, images, etc.

`templates` - Contains the html templates for the project. I prefer to set up templates in the root folder and configure the `TEMPLATES` setting in the `settings.py` file to point to the templates folder.

`mainapp` - The main app folder.

`mainapp\urls.py` - Contains the urls for the main app.

`mainapp\views.py` - Contains the views for the main app.

`mainapp\tests.py` - Contains the tests for the main app.

`mainapp\models.py` - Contains the models for the main app such as `Crypto` and `Portfolio`.

`mainapp\forms.py` - Contains the forms for the main app such as `CustomUserCreationForm`

`mainapp\migrations` - Contains the migrations for the main app.

`mainapp\signals.py` - Contains the `create_profile` signal once a user is created.

## Available Endpoints [URLs]

```
localhost:8000/
localhost:8000/login
localhost:8000/logout
localhost:8000/signup
localhost:8000/signup/str:referral_code
localhost:8000/portfolio
localhost:8000/search
localhost:8000/add_to_portfolio
localhost:8000/delete_from_portfolio/int:pk
localhost:8000/password_reset
localhost:8000/password_reset_done
localhost:8000/password_reset_confirm/<uidb64>/<token>
localhost:8000/password_reset_complete 
localhost:8000/admin
```

## Test Driven Development Approach Explained

In Django, automated testing can be performed at three levels: URL testing, model testing, and view testing.

#### URL Testing

URL testing in Django is used to check if the endpoints specified in the URL patterns are correctly configured and pointing to the appropriate views. This is important because if an endpoint is incorrect or pointing to the wrong view, the application will not be able to process the request, leading to errors or incorrect behavior. URL testing is typically performed using the Django Client class, which simulates a web client and allows the developer to send requests to the application.

#### Model Testing

Model testing in Django is used to check if the data stored in the database matches the expected schema and constraints specified in the models.py file. It helps ensure that the application is storing and retrieving data correctly and that the database is working as expected. Model testing is typically performed using the Django TestCase class and its various assertion methods, which allow the developer to create test data, save it to the database, and verify that the data has been saved correctly.

#### View Testing

View testing in Django is used to check if the business logic defined in the views.py file is functioning correctly. It is used to test whether the views are handling requests as expected and returning the appropriate responses. View testing is typically performed using the Django TestCase class and its various assertion methods, which allow the developer to simulate requests and verify the responses.

> For this crypto-wallet app, I used all three types of automated testing.

**For URL testing**, I created a series of test cases that used the Django Client class to simulate requests to various endpoints in the application. Each test case sent a request to the endpoint and verified that the response was the expected template.

**For model testing**, I created a series of test cases that used the Django TestCase class to create test data, save it to the database, and verify that it had been saved correctly. Each test case tested a specific model or relationship between models to ensure that the data was being stored and retrieved correctly.

**For view testing**, I created a series of test cases that used the Django TestCase class to simulate requests to various views in the application. Each test case sent a request to the view and verified that the response was the expected result.

>Total Test Cases Written: 66
>Passing Test Cases: 64
>Failing Test Cases: 2 [Unable to fix the failing test cases due to time constraints]

## Some Notes

- I used the `django-crispy-forms` package to style the forms.
- In the search box on the home page, the closest matching cryptocurrency is shown on the results page.
- I have set the bonus of a referral system to a static value of 100 per referral on successful signup. This can be implemented different if needed. Maybe a percentage of the total value of the portfolio of the person who referred the new user.
- I chose to go with built-in Django authentication system instead of using a third-party package like `django-allauth` due to time constraints.
- I used the build in auth.User model for the user model. I could have created a custom user model but I wanted to focus more on the business logic and the ORM queries.
- **IMPORTANT:** Constantly refreshing the home page will result in too many API calls and the contents of the cryptocurrency table might disappear until a minute or two, this is because of the API rate limit. Hence, constant refreshing is not recommended.

## Challenges I Faced

- Designing the database schema was a bit challenging. I had to think about the relationships between the models and how to store the data in the database.
- Did not previously know about ways to do view testing in Django. I had to do some research to find out how to do it. But it worked out well.
- Had trouble with JavaScript to make the search form dynamic, originally I wanted to allow users to type and show autocomplete suggestions but had to settle for a search button that redirects to the search results page due to time constraints.
- Working on business logic to update the portfolio and calculate the total value of the portfolio. It proved to be a good ORM exercise and I got a chance to revise my ORM queries.

## What I would do differently if I had more time

- Use a proper production-ready database like Postgres instead of the default sqlite database.
- Make the code more functional and modular, especially in views.py
- Improve the admin panel to make it more user-friendly.
- Add more tests to cover more edge cases. Currently I have 90% coverage but I would like to add more tests to cover more edge cases.
- Improve the UI, add tags to django messages and make the messages more user-friendly.
- Implement Caching to improve performance and reduce API calls.

## Screenshots [Feature Checklist]

#### Admin Panel - Users

![Screenshot 1](https://github.com/HighnessAtharva/django-crypto-app/blob/main/assets/admin-1.png?raw=true)

#### Admin Panel - Cryptocurrencies

![Screenshot 1](https://github.com/HighnessAtharva/django-crypto-app/blob/main/assets/admin-2.png?raw=true)

#### Admin Panel - Referrals

![Screenshot 1](https://github.com/HighnessAtharva/django-crypto-app/blob/main/assets/admin-3.png?raw=true)

#### Admin Panel - Portfolio

![Screenshot 1](https://github.com/HighnessAtharva/django-crypto-app/blob/main/assets/admin-4.png?raw=true)

#### Admin Panel - Referrals

![Screenshot 1](https://github.com/HighnessAtharva/django-crypto-app/blob/main/assets/admin-5.png?raw=true)

#### Login Screen

![Screenshot 1](https://github.com/HighnessAtharva/django-crypto-app/blob/main/assets/Login.png?raw=true)

#### Signup Screen

![Screenshot 1](https://github.com/HighnessAtharva/django-crypto-app/blob/main/assets/signup.png?raw=true)

#### Password Reset Email

![Screenshot 1](https://github.com/HighnessAtharva/django-crypto-app/blob/main/assets/password-reset-email.png?raw=true)

#### Email Confirmation

![Screenshot 1](https://github.com/HighnessAtharva/django-crypto-app/blob/main/assets/password-reset-success.png?raw=true)

#### Forgot Password Page

![Screenshot 1](https://github.com/HighnessAtharva/django-crypto-app/blob/main/assets/reset-password.png?raw=true)

#### Add Currency / Search Result Page

![Screenshot 1](https://github.com/HighnessAtharva/django-crypto-app/blob/main/assets/add-currency.png?raw=true)

#### Referral Signup Bonus

![Screenshot 1](https://github.com/HighnessAtharva/django-crypto-app/blob/main/assets/bonus.png?raw=true)

#### Home Page [No Login]

![Screenshot 1](https://github.com/HighnessAtharva/django-crypto-app/blob/main/assets/home-1.png?raw=true)

#### Home Page Bottom [Login]

![Screenshot 1](https://github.com/HighnessAtharva/django-crypto-app/blob/main/assets/home-blank.png?raw=true)

#### Search Page [Add or Update Quantity]

![Screenshot 1](https://github.com/HighnessAtharva/django-crypto-app/blob/main/assets/search-2.png?raw=true)

#### Home Page Bottom [Logged In] - Shows 24 Hour Price Change

![Screenshot 1](https://github.com/HighnessAtharva/django-crypto-app/blob/main/assets/user-price-change.png?raw=true)

#### Wallet Page

![Screenshot 1](https://github.com/HighnessAtharva/django-crypto-app/blob/main/assets/wallet-1.png?raw=true)

#### Wallet Page Cont

![Screenshot 1](https://github.com/HighnessAtharva/django-crypto-app/blob/main/assets/wallet-2.png?raw=true)

#### Wallet Page [No Currencies Added, No Referrals]

![Screenshot 1](https://github.com/HighnessAtharva/django-crypto-app/blob/main/assets/wallet-blank.png?raw=true)
