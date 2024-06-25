# scheduler_app

```markdown
# Environment and Dependencies Setup Tutorial

Special Thanks to original contributors: Nico, Cody, and Robert. This was our group project in class at Oregon State University.

All changes after 6/24/24 on this repository are an individual effort by myself.

## Installing from Scratch

### 1. Python Environment
- Within the top directory of the app (`scheduler_app`), type:
  ```bash
  python -m venv env
  source env/bin/activate
  ```
- You should now be in the environment (`env`).
- Within `env`, type:
  ```bash
  pip install flask
  pip install flask_pymongo
  pip install flask_login
  pip install flask_bcrypt
  ```
- This should conclude dependencies, but it is OPTIONAL to type:
  ```bash
  pip install -r App/requirements.txt
  ```
- At this point, the Flask web application can be run. Type:
  ```bash
  python App/app.py
  ```
- Go to `http://localhost:5000`.
- Register a user!

### 2. Docker and MongoDB
- Download the Docker Desktop ([https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)) and run it.
- Verify the install by typing in a new terminal:
  ```bash
  docker --version
  ```
- Next, to run the MongoDB container, type:
  ```bash
  docker pull mongo
  docker run -d -p 27017:27017 --name mongodb mongo
  ```
- Now, to enter the MongoDB bash, type:
  ```bash
  docker exec -it mongodb bash
  ```
- This should take you to the MongoDB bash and look like `root@something...`, then type:
  ```bash
  mongosh
  ```
- If it says something like `test>`, then you're in! Switch to `app.py`'s database:
  ```bash
  use Scheduler
  show collections
  ```
- If you registered a user on the web app, then `users` should be present! You did it!

## Developer Notes for `scheduler_alg.py`

This program implements an employee scheduling system using a `ScheduleManager` class. The system allows for scheduling employees based on their availability for different time slots throughout the week (Monday to Friday). The program maintains a schedule represented as a nested dictionary, where keys are days of the week and values are dictionaries mapping time slots (in 25-unit increments) to lists of scheduled employees.

### How Time is Represented in this Program
- 25 units = 15 minutes.
- Examples: 
  - 1300 = 1:00pm
  - 1325 = 1:15pm
  - 1350 = 1:30pm
  - 1375 = 1:45pm

### Class Overview

#### `ScheduleManager` Class
Manages the scheduling of employees and maintains the current schedule.

##### Attributes
- `schedule`: Nested dictionary representing the schedule. The outer keys are days of the week ("Monday", "Tuesday", etc.), and the inner dictionaries map time slots (in 25-unit increments) to lists of scheduled employees.
- `employee_hours`: Dictionary tracking the total hours worked by each employee.

##### Methods
- `schedule_employee(availability, identifier)`: Schedules an employee with a unique identifier based on their availability.
- `display_schedule()`: Displays the current schedule with scheduled employees for each time slot.

### How It Works

#### Initialization
- The `ScheduleManager` class is initialized with an empty schedule and an empty dictionary to track employee hours.

#### Scheduling Employees
- Employees are scheduled using the `schedule_employee` method. This method takes an availability dictionary containing the availability of an employee for each day of the week ("Monday", "Tuesday", etc.) and a unique identifier (e.g., employee ID or name) for the scheduled individual.
- The method iterates over the days of the week and available time segments, checking if the time slot is available and if the employee has not exceeded their maximum allowed hours.
- If the conditions are met, the employee is scheduled in the respective time slot, and their total hours are updated in the `employee_hours` dictionary.

#### Displaying Schedule
- The `display_schedule` method is used to visualize the current schedule. It prints the scheduled employees for each time slot within each day of the week.

### Test Cases
- Test cases are provided with randomized availability for each day of the week. These test cases simulate different scenarios where employees have varying availability throughout the week.

### Randomization and Shuffling
- To introduce randomness into the scheduling process, the program shuffles the order of days when processing availability and shuffles the key/value pairs within the test cases dictionary. This ensures that the scheduling is distributed randomly across days and time slots.

### Key Points Accounted For
- Multiple available times within the same day.
- Names for employees (in separate list that must be same index as availability).
- Draws from data in the database.
- Prints a decently readable generated schedule.

### Key Points NOT Implemented
- Rotations (this means also no Network Security Monitoring full coverage).
- Document parsing.
- Visual schedule representation.
- Data export.
- Optimization.
- Checks for usernames, schedules list to be of the same length.