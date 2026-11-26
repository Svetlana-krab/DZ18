import json
import os

FILE_NAME = "patients.json"

class PatientModel:
    def __init__(self):
        self.patients = []
        self.load()

    def load(self):
        if os.path.exists(FILE_NAME):
            try:
                with open(FILE_NAME, "r", encoding="utf-8") as f:
                    self.patients = json.load(f)
            except:
                self.patients = []

    def save(self):
        with open(FILE_NAME, "w", encoding="utf-8") as f:
            json.dump(self.patients, f, ensure_ascii=False, indent=4)

    def add(self, patient):
        self.patients.append(patient)
        self.save()

    def remove_by_index(self, idx):
        if 0 <= idx < len(self.patients):
            self.patients.pop(idx)
            self.save()

    def get_all(self):
        return self.patients

    def calculate_bmi(self, weight, height_cm):
        if height_cm <= 0:
            return 0
        height_m = height_cm / 100
        return round(weight / (height_m ** 2), 1)