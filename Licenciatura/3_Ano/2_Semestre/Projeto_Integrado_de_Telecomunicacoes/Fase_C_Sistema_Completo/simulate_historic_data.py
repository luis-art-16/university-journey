# Import required libraries
import random
from datetime import datetime, timedelta
from app import create_app
from app.services.database_service import db
from app.models import Patient, PatientReading, FallEvent

# Create Flask application context
app = create_app()

def generate_realistic_values(base_date):
    """
    Generates realistic health metrics with day/night patterns
    Args:
        base_date (datetime): The timestamp for which to generate values
    Returns:
        dict: Dictionary with keys: heart_rate, spo2, temperature
    """
    hour = base_date.hour

    if 8 <= hour < 20:
        heart_rate = random.randint(70, 100)
        spo2 = random.randint(96, 100)
        temp = round(random.uniform(36.5, 37.2), 1)
    else:
        heart_rate = random.randint(60, 80)
        spo2 = random.randint(95, 99)
        temp = round(random.uniform(36.0, 36.8), 1)

    return {
        'heart_rate': max(50, min(heart_rate + random.randint(-5, 5), 120)),
        'spo2': max(90, min(spo2 + random.randint(-1, 1), 100)),
        'temperature': max(35.5, min(temp + round(random.uniform(-0.2, 0.2), 1), 38.5))
    }

def backfill_10min_data():
    """
    Generates and inserts realistic patient data at 10-minute intervals
    for the past 30 days, splitting out fall events.
    """
    with app.app_context():
        patients = Patient.query.all()
        if not patients:
            print("No patients found!")
            return

        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)

        for patient in patients:
            print(f"Backfilling data for {patient.medical_record_number}...")

            # Clear existing readings and fall events for this patient
            PatientReading.query.filter_by(patient_id=patient.id).delete()
            FallEvent.query.filter_by(patient_id=patient.id).delete()

            current = start_date
            while current <= end_date:
                values = generate_realistic_values(current)

                # Create and add the vital-reading
                reading = PatientReading(
                    patient_id=patient.id,
                    timestamp=current,
                    heart_rate=values['heart_rate'],
                    spo2=values['spo2'],
                    temperature=values['temperature']
                )
                db.session.add(reading)

                # Simulate a rare fall event (1% chance)
                if random.random() < 0.01:
                    severity = random.randint(1, 5)
                    status = random.choice(['pending', 'reviewed', 'resolved'])
                    
                    # Create and add FallEvent
                    fall = FallEvent(
                        patient_id=patient.id,
                        timestamp=current,
                        severity=severity,
                        status=status
                    )
                    db.session.add(fall)
                    print(f"Fall detected for {patient.medical_record_number} at {current} (Severity: {severity}, Status: {status})")

                current += timedelta(minutes=10)

        db.session.commit()
        print(f"Backfilled 10-minute data for {len(patients)} patients from {start_date} to {end_date}")

if __name__ == "__main__":
    backfill_10min_data()