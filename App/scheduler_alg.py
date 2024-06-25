import random
from pymongo import MongoClient

class ScheduleManager:
    def __init__(self, db):
        self.db = db
        self.schedule = {
            "Monday": {t: [] for t in range(700, 1900, 25)},
            "Tuesday": {t: [] for t in range(700, 1900, 25)},
            "Wednesday": {t: [] for t in range(700, 1900, 25)},
            "Thursday": {t: [] for t in range(700, 1900, 25)},
            "Friday": {t: [] for t in range(700, 1900, 25)},
        }
        self.employee_hours = {}

    def schedule_employee(self, availability, identifier):
        days_to_process = list(availability.keys())
        random.shuffle(days_to_process)
        for day in days_to_process:
            segments = availability[day]
            random.shuffle(segments)
            for start_time, end_time in segments:
                for t in range(start_time, end_time, 25):
                    if t in self.schedule[day] and len(self.schedule[day][t]) < 10:
                        if identifier in self.employee_hours and self.employee_hours[identifier] >= 11 * 4:
                            return
                        else:
                            self.employee_hours.setdefault(identifier, 0)
                        self.schedule[day][t].append(identifier)
                        self.employee_hours[identifier] += 1

    def display_schedule(self):
        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        schedule_str = "Current Schedule:\n"
        for day in days_of_week:
            schedule_str += f"{day}:\n"
            for t in range(700, 1900, 25):
                if t in self.schedule[day]:
                    scheduled_individuals = self.schedule[day][t]
                    if scheduled_individuals:
                        schedule_str += f"  {t} - {t + 25}: {', '.join(map(str, scheduled_individuals))}\n"
                    else:
                        schedule_str += f"  {t} - {t + 25}: No employees scheduled\n"
        return schedule_str

    def convert_time_to_int(self, time_str):
        hours, minutes = map(int, time_str.split(":"))
        minutes = str(minutes).zfill(2)
        if minutes == "00":
            minutes = "00"
        elif minutes == "15":
            minutes = "25"
        elif minutes == "30":
            minutes = "50"
        elif minutes == "45":
            minutes = "75"
        result = str(hours) + minutes
        return int(result)

    def retrieve_schedule(self):
        schedule_collection = self.db["schedule"]
        user_collection = self.db["users"]
        users = list(user_collection.find())
        user_dict = {str(user["_id"]): user["username"] for user in users}
        schedules = list(schedule_collection.find())
        user_schedules = {}
        for entry in schedules:
            user_id = str(entry["user_id"])
            day = entry["day"]
            in_time = self.convert_time_to_int(entry["in_time"])
            out_time = self.convert_time_to_int(entry["out_time"])
            username = user_dict.get(user_id, "Unknown")
            if user_id not in user_schedules:
                user_schedules[user_id] = {"username": username, "schedule": {}}
            if day not in user_schedules[user_id]["schedule"]:
                user_schedules[user_id]["schedule"][day] = []
            user_schedules[user_id]["schedule"][day].append((in_time, out_time))
        result = []
        for user_id, data in user_schedules.items():
            result.append({"user_id": user_id, "username": data["username"], "schedule": data["schedule"]})
        return result
    
    def get_usernames_and_schedules(self):
        schedule_data = self.retrieve_schedule()
        usernames = []
        schedules = []
        for user_data in schedule_data:
            usernames.append(user_data["username"])
            schedules.append(user_data["schedule"])
        return usernames, schedules

    def randomize_scheduling(self, names, availabilities, schedule_manager):
        random.shuffle(availabilities)
        for idx, availability in enumerate(availabilities):
            if idx < len(names):
                employee_name = names[idx]
            else:
                employee_name = f"Employee_{idx + 1}"
            schedule_manager.schedule_employee(availability, employee_name)

    def get_schedule(self):
        """
        Returns the current schedule as a dictionary.
        """
        return self.schedule
