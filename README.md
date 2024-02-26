# Find Match
Find Match is a web system to manage sports events, allowing organizers to manage the subscriptions, and Team Leaders to subscribe to events. The system ensures that all subscriptions are valid. This project was developed for the Software Engineering class, for the Computer Science course at UFRGS, during the 2023/2 semester.

## Features

**Leader:**
- Manage teams
- Subscribe team to competition

**Organizer:**
- Create and Manage events
- Register event results
- Get reports about event subscriptions

## How to install and execute the application
First clone the repository and then execute the following commands

```sh
pip install -r requirements.txt # Installing dependencies
cd server
python3 manage.py migrate # Setup DB
python3 manage.py create_groups # Create required permissions and roles
python3 manage.py runserver
```
