"""
TODO: Implement the Patient class.
Please import and use the config and db config variables.

The attributes for this class should be the same as the columns in the PATIENTS_TABLE.

The Object Arguments should only be name , gender and age.
Rest of the attributes should be set within the class.

-> for id use uuid4 to generate a unique id for each patient.
-> for checkin and checkout use the current date and time.

There should be a method to update the patient's room and ward. validation should be used.(config is given)

Validation should be done for all of the variables in config and db_config.

There should be a method to commit that patient to the database using the api_controller.
"""

import uuid
from datetime import datetime
from api_controller import PatientAPIController
from config import GENDERS, WARD_NUMBERS, ROOM_NUMBERS, API_CONTROLLER_URL
from patient_db_config import PATIENT_COLUMN_NAMES
import requests

class Patient:
    def __init__(self, name, gender, age):
        self.patient_id = str(uuid.uuid4())
        self.patient_name = self.validate_name(name)
        self.patient_gender = self.validate_gender(gender)
        self.patient_age = self.validate_age(age)
        self.patient_checkin = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.patient_checkou = None
        self.patient_ward = None
        self.patient_room = None


    def validate_name(self, name):
        if not isinstance(name, str):
            raise ValueError("Name must be a string")
        return name

    def validate_gender(self, gender):
        if gender not in GENDERS:
            raise ValueError("Invalid gender")
        return gender

    def validate_age(self, age):
        try:
            age = int(age)
            if age < 0:
                raise ValueError("Age cannot be negative")
            return age
        except ValueError:
            raise ValueError("Age must be an integer")

    def validate_ward(self, ward):
        if ward not in WARD_NUMBERS:
            raise ValueError("Invalid ward number")
        return ward
    
    def set_checkout_info(self, ward, room):
        self.patient_checkout = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.patient_ward = self.validate_ward(ward)
        self.patient_room = self.validate_room(room)

    def validate_room(self, ward, room):
        if room not in ROOM_NUMBERS[ward]:
            raise ValueError("Invalid room number for the ward")
        return room

    def update_room_and_ward(self, ward, room):
        if (ward in WARD_NUMBERS and room in ROOM_NUMBERS[ward]):
            self.patient_ward = ward
            self.patient_room = room
            print("Room and ward updated successfully.")
        else:
            print("Invalid ward or room number.")


    def commit_to_database(self):
            data = {
                
                "patient_name": self.patient_name,
                "patient_age": self.patient_age,
                "patient_gender": self.patient_gender,
                "patient_ward": self.patient_ward,
                "patient_room": self.patient_room
            }
            response = requests.post(f"{API_CONTROLLER_URL}/patients", json=data)
            if response.status_code == 200:
                print("Patient data committed successfully.")
                response_data = response.json()
                self.patient_id = response_data.get("patient_id")
                self.patient_checkin = response_data.get("patient_checkin")
            else:
                print("Failed to commit patient data to the database.")
