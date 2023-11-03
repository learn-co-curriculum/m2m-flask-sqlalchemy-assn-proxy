from flask import Flask, abort, make_response, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import Appointment, Doctor, Patient, db
from werkzeug.exceptions import NotFound

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

# monkey-patching flask-restful's error_router to substitute Flask's native app.errorhandler
Api.error_router = lambda self, handler, e: handler(e)
api = Api(app)


class Patients(Resource):
    def get(self):
        patients = db.session.scalars(db.select(Patient))
        return [patient.to_dict() for patient in patients]


class PatientById(Resource):
    def get(self, id):
        patient = db.session.scalars(
            db.select(Patient).where(Patient.id == id)
        ).one_or_none()
        if patient is None:
            raise NotFound(f"Patient {id} not found")
        return patient.to_dict()


class Doctors(Resource):
    def get(self):
        doctors = Doctor.query.all()
        return [doctor.to_dict() for doctor in doctors]


class DoctorsById(Resource):
    def get(self, id):
        doctor = Doctor.query.get(id)
        if doctor is None:
            raise NotFound(f"Doctor {id} not found")
        return doctor.to_dict()


api.add_resource(Patients, "/patients")
api.add_resource(PatientById, "/patients/<int:id>")
api.add_resource(Doctors, "/doctors")
api.add_resource(DoctorsById, "/doctors/<int:id>")


if __name__ == "__main__":
    app.run(port=5555, debug=True)
