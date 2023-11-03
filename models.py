from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()


class Patient(db.Model, SerializerMixin):
    __tablename__ = "patients"

    serialize_rules = (
        "-appointments.patient",
        "-appointments.doctor",
        "doctors",
        "-doctors.appointments",
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    appointments = db.relationship("Appointment", back_populates="patient")
    doctors = association_proxy("appointments", "doctor")

    def __repr__(self):
        return f"<Patient {self.name}>"


class Doctor(db.Model, SerializerMixin):
    __tablename__ = "doctors"

    serialize_rules = ("-appointments.doctor", "-appointments.patient")

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    specialty = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    appointments = db.relationship("Appointment", back_populates="doctor")
    patients = association_proxy("appointments", "patient")

    def __repr__(self):
        return f"<Doctor {self.name}>"


class Appointment(db.Model, SerializerMixin):
    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    patient = db.relationship("Patient", back_populates="appointments")
    doctor = db.relationship("Doctor", back_populates="appointments")

    def __repr__(self):
        return f"<Appointment {self.id}>"
