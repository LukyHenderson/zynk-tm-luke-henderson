# **Zynk Task Management Application**

A functional Django-based task management application that demonstrates the integration of Django, Redis, Celery, Django-Redis, and Tailwind CSS. This app allows users to efficiently manage their tasks by creating, viewing, marking completion, categorizing, and receiving automatic reminders.

## **Overview**

This Application fulfills the requirements specified in the Zynk Python Developer Test by:
Implementing Django models, views, URLs, and templates;
Utilizing Celery for background task processing;
Using Redis both as the message broker and as a caching mechanism via Django-Redis;
Enhancing the user interface using Tailwind CSS.

## **Features**

Task Management: Create, view, update, complete, flag, categorize, and delete tasks.

User Authentication: Secure login, signup, and logout functionalities.

Background Task Reminders: Automatic email reminders triggered by Celery tasks. (emails currently disabled as app password is revoked, to test this create an app password with your google account and place it on projectTM/settings.py line 138 )

Caching: Efficient caching of task lists for improved performance.

Enhanced UI: Clean and responsive design implemented with Tailwind CSS.

## **Project Setup & Installation**

Follow these steps to set up and run the project locally:

**_Step 1: Clone the Repository_**

git clone [your-repository-url]
cd zynk

**_Step 2: Install Dependencies_**

Ensure Python 3.10 or newer is installed.

Install required packages:

pip install -r requirements.txt

**_Step 3: Set Up Redis_**

Run Redis server locally using Docker:

docker run -d --name redis -p 6379:6379 redis

**_Step 4: Apply Database Migrations_**

python manage.py migrate

**_Step 5: Start Celery Worker_**

Run Celery worker (use solo pool on Windows):

celery -A projectTM worker -l info --pool=solo

**_Step 6: Run Django Development Server_**

python manage.py runserver

The application will be accessible at http://127.0.0.1:8000/

**_Step 7: Access Django Admin (optional)_**

Admin credentials:

Username: admin

Email: admin@example.com

Password: Administrator1234

**_Step 8: Auto Email Functionality (optional)_**

Emails currently disabled as app password was revoked, to test this create an app password with your google account and place it on projectTM/settings.py line 138. You will also need to replace the email adress on line 137.

## **Technology Stack**

Django: Web framework handling backend logic and MVC architecture.

Redis: Message broker for Celery and caching backend for Django.

Celery: Task queue system for scheduling asynchronous tasks (e.g., sending reminders).

Django-Redis: Django integration for using Redis as cache backend.

Tailwind CSS: CSS framework for a responsive and modern user interface.

## **Project Structure**

appTM/models.py: Defines the Task model and additional customizations.

appTM/views.py: Contains views for task operations and user authentication.

appTM/tasks.py: Celery task definitions for asynchronous operations.

appTM/forms.py: Django forms for creating tasks and managing user signup.

appTM/urls.py: URL routing for the application views.

appTM/templates/: HTML templates powered by Tailwind CSS.

runcommands.txt: Quick reference for essential terminal commands.

requirements.txt: Project dependencies for easy setup.

## **Requirements**

Django ~= 5.2

Celery ~= 5.5.1

Redis ~= 5.2.1

Django-Redis ~= 5.2.0

## **Additional Notes**

The application includes caching mechanisms to improve performance, especially when handling a large number of tasks.
User authentication ensures task data security and personalization.
Background tasks efficiently manage reminders and user notifications without interrupting the main application.

## **License**

This project is licensed under the [MIT License](./LICENSE).

## **Author**

Luke Henderson

luky.henderson@gmail.com

https://github.com/Darkrai6666

https://www.linkedin.com/in/luke-henderson-dev/
