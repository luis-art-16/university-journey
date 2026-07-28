from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    full_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.now())

    # One-to-one relationships
    patient = db.relationship('Patient', back_populates='user', uselist=False)
    doctor = db.relationship('Doctor', back_populates='user', uselist=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Doctor(db.Model):
    __tablename__ = 'doctors'

    id = db.Column(db.Integer, primary_key=True)
    specialization = db.Column(db.String(100))
    license_number = db.Column(db.String(50), unique=True, nullable=False)
    department = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False)

    # One-to-one to User
    user = db.relationship('User', back_populates='doctor')
    # One-to-many: Doctor -> Patients
    patients = db.relationship('Patient', back_populates='doctor', cascade='all, delete-orphan')

class Patient(db.Model):
    __tablename__ = 'patients'

    id = db.Column(db.Integer, primary_key=True)
    medical_record_number = db.Column(db.String(50), unique=True, nullable=False)
    date_of_birth = db.Column(db.String(20))
    gender = db.Column(db.String(10))
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    admission_date = db.Column(db.DateTime, default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id', ondelete='SET NULL'))

    # One-to-one to User
    user = db.relationship('User', back_populates='patient')
    # Many-to-one: Patient -> Doctor
    doctor = db.relationship('Doctor', back_populates='patients')
    # One-to-many: Patient -> Readings & Falls
    readings = db.relationship(
        'PatientReading', back_populates='patient',
        cascade='all, delete-orphan'
    )
    falls = db.relationship(
        'FallEvent', back_populates='patient',
        cascade='all, delete-orphan'
    )

class PatientReading(db.Model):
    __tablename__ = 'patient_readings'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    patient_id = db.Column(
        db.Integer,
        db.ForeignKey('patients.id', ondelete='CASCADE'),
        nullable=False
    )
    heart_rate = db.Column(db.Integer)
    spo2 = db.Column(db.Integer)
    temperature = db.Column(db.Float)

    # Many-to-one: Reading -> Patient
    patient = db.relationship('Patient', back_populates='readings')

class FallEvent(db.Model):
    __tablename__ = 'fall_events'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    severity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    patient_id = db.Column(
        db.Integer,
        db.ForeignKey('patients.id', ondelete='CASCADE'),
        nullable=False
    )

    # Many-to-one: FallEvent -> Patient
    patient = db.relationship('Patient', back_populates='falls')
