from app.models import Alert, Patient
from app import db

# Get first patient
patient = Patient.query.first()

# Create test alert
test_alert = Alert(
    patient_id=patient.id,
    alert_type='heart_rate',
    severity='high',
    message='TEST ALERT: High heart rate (120 bpm)',
    is_read=False
)
db.session.add(test_alert)
db.session.commit()