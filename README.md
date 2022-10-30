# TutorBook Server

A Django backend serving json data to the TutorBook frontend. This was always going to be a challenge as Django was very enw to me when the project began. 

## Tech Stack

1. Python with Django
2. Django Rest Framework
3. PostGres DB
4. Firebase Admin
5. Heroku deployment

## Approach

I spent the first week of my project planning the database schema and backend api routes. This stage sketched out the initial functionality and how the backend would serve various forms of data. During this stage, I also prototyped my frontend and came up with a rudimentary prototype on figma. 

After this initial planning phase, I spent time setting up the Django project and the database and wrote the initial models, views, routes and serializers. These subsequently changed somewhat as I progressed with the frontend.

My initial deployment was done with 2 weeks to spare to iron out the inevitable issues that come with deployment.

## Issues Faced

![One does not simply start coding in Django](http://www.quickmeme.com/img/84/84bdee48fbd15efe214193d08da213e7a57fcacc993959b6e65fb2599538f1df.jpg)


1. Django Rest Framework can be very opaque at times. If I was to start again using Django as a backend, I would write all the views from scratch as opposed to using generic views. It is much easier to debug and see what is going on when writing your own views.
2. Django generally as an API backend serving JSON files only is a bit overkill. As a monolithic app, I can see its value, but as a backend only, it causes more problems than it solves. A more lightweight framework (such as Flask or Express) would be better for this kind of work.
3. Django deployment on Heroku was absolutely hellish. The Heroku and Django documentation on deployment is sparse and inconsistent. Only after spending several hours fiddling with settings did I mange to get it to work. Deploying via a docker image would be better.
4. Backend integration with Firebase was not easy, neither was it well documented. Writing a custom authentication class for Firebase when not having a complete idea over how authentication classes work took a lot of time and effort.

## Things I Liked

1. Relational databases are incredibly powerful and once the ORM in Django was sussed out, were a pleasure to implement. I will certainly look to use a relational database over MongoDB in the future unless there is a specific case for MongoDB.
2. Django Rest Framework documentation was well written and logically laid out whilst not being too overwhelming (like Django's documentation).

## Things To Do

1. Implement a backend refresh with Firebase Admin for when a user confirms their email address.
2. Implement a backend refresh with Firebase Admin for when a user changes their email.
3. Migrate the DB to use the Firebase UID for each user instead of a DB generated UUID so that less API calls are needed.
4. Implement a route that takes in search parameters so that a user can search assignments and tutors. 

## Initial Planned Routes

These were the initial planned routes but they have changed slightly in development.

https://docs.google.com/spreadsheets/d/1IqUbYhrEhnjoZTcGKqz4sQ0_mkvm-uXYQICVVKgq-eA/edit?usp=sharing
