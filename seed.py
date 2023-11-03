from datetime import datetime

from app import app
from faker import Faker
from models import Appointment, Doctor, Patient, db

fake = Faker()

with app.app_context():
    print("Dropping tables...")
    Appointment.query.delete()
    Patient.query.delete()
    Doctor.query.delete()

    patients = []
    doctors = []

    print("Seeding tables...")
    for _ in range(10):
        patient = Patient(
            name=fake.name(),
            dob=fake.date_between(start_date="-90y", end_date="-18y"),
        )
        patients.append(patient)
    db.session.add_all(patients)

    for _ in range(5):
        doctor = Doctor(
            name=fake.name(),
            specialty=fake.job(),
        )
        doctors.append(doctor)
    db.session.add_all(doctors)

    for _ in range(20):
        appointment = Appointment(
            patient=fake.random_element(patients),
            doctor=fake.random_element(doctors),
            date=fake.date_between(start_date="today", end_date="+1y"),
            time=datetime.strptime(fake.time(), "%H:%M:%S").time(),
        )
        db.session.add(appointment)

    db.session.commit()
    print("Done!")
