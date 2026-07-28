import random
from datetime import datetime, timedelta
from app import create_app
from app.services.database_service import db
from app.models import Patient, PatientReading

app = create_app()

def generate_realistic_values(base_date):
    """Generate health data with day/night patterns and realistic falls"""
    hour = base_date.hour
    if 8 <= hour < 20:  # Daytime (more active)
        heart_rate = random.randint(70, 100)
        spo2 = random.randint(96, 100)
        temp = round(random.uniform(36.5, 37.2), 1)
    else:  # Nighttime (calmer)
        heart_rate = random.randint(60, 80)
        spo2 = random.randint(95, 99)
        temp = round(random.uniform(36.0, 36.8), 1)
    
    # Add variability
    values = {
        'heart_rate': max(50, min(heart_rate + random.randint(-5, 5), 120)),
        'spo2': max(90, min(spo2 + random.randint(-1, 1), 100)),
        'temperature': max(35.5, min(temp + round(random.uniform(-0.2, 0.2), 1), 38.5)),
        'fall_detected': False,  # Default to no fall
        'fall_severity': None    # Default to no severity
    }

    # Generate fall with 1% probability
    if random.random() < 0.01:  # 1% chance of fall
        values['fall_detected'] = True
        values['fall_severity'] = random.randint(1, 5)  # Severity levels 1-5
        # Simulate physiological response to fall
        values['heart_rate'] = min(140, values['heart_rate'] + random.randint(20, 40))
        values['spo2'] = max(85, values['spo2'] - random.randint(1, 5))
    
    return values

def backfill_10min_data():
    with app.app_context():
        patients = Patient.query.all()
        if not patients:
            print("No patients found!")
            return

        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)

        for patient in patients:
            print(f"Backfilling data for {patient.patient_id}...")
            PatientReading.query.filter_by(patient_id=patient.id).delete()  # Optional: Clear old data

            current_date = start_date
            while current_date <= end_date:
                values = generate_realistic_values(current_date)
                reading = PatientReading(
                    patient_id=patient.id,
                    timestamp=current_date,
                    **values
                )
                db.session.add(reading)
                current_date += timedelta(minutes=10)  # Generate data every 10 minutes

                # Print fall incidents for verification
                if values['fall_detected']:
                    print(f"Fall detected for {patient.patient_id} at {current_date} (Severity: {values['fall_severity']})")

        db.session.commit()
        print(f"Backfilled 10-minute data for {len(patients)} patients from {start_date} to {end_date}")

if __name__ == "__main__":
    backfill_10min_data()