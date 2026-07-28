# simulator.py

import time
import json
import random
from datetime import datetime
from app import create_app
from app.services.mqtt_service import mqtt_service
from app.services.database_service import get_db_session
from app.models import Patient

# Initialize Flask application
app = create_app()

broker = "127.0.0.1"
port = 1883
topic_prefix = "health_monitoring"

def generate_heart_rate(base=70):
    return random.randint(max(50, base-20), min(120, base+20))

def generate_spo2(base=97):
    return random.randint(max(90, base-5), min(100, base+2))

def generate_temperature(base=36.8):
    return round(random.uniform(max(35.5, base-1), min(38.5, base+1)), 1)

def get_all_patient_ids():
    with app.app_context():
        db_session = get_db_session()
        try:
            patients = db_session.query(Patient).all()
            return [p.medical_record_number for p in patients]
        finally:
            db_session.close()

def generate_fall_reading(base_values):
    severity = random.choices([1,2,3,4,5], weights=[35,30,20,10,5], k=1)[0]
    return {
        **base_values,
        "fall_detected": True,
        "fall_severity": severity,
        "status": random.choice(['pending', 'reviewed', 'resolved']),
        "heart_rate": min(140, base_values["heart_rate"] + severity*5 + random.randint(5,10)),
        "spo2": max(80, base_values["spo2"] - severity - random.randint(1,3)),
        "temperature": base_values["temperature"] + round(severity * 0.1, 1)
    }

def simulate_readings():
    patient_mrns = get_all_patient_ids()
    if not patient_mrns:
        print("❌ No patients found! Exiting...")
        return

    print(f"📋 Found {len(patient_mrns)} patients. Starting simulation...")

    # Garante que o cliente MQTT está inicializado
    while True:
        try:
            mqtt_service.ensure_connection()  # aqui o client será criado se None
            break
        except Exception as e:
            print(f"⚠️ MQTT initial connection failed: {e}. Retrying in 3s...")
            time.sleep(3)

    while True:
        timestamp = datetime.now().isoformat()
        for mrn in patient_mrns:
            base_reading = {
                "timestamp": timestamp,
                "heart_rate": generate_heart_rate(),
                "spo2": generate_spo2(),
                "temperature": generate_temperature(),
            }

            if random.random() < 0.01:
                severity = random.choices([1,2,3,4,5], weights=[35,30,20,10,5])[0]
                reading = {
                    **base_reading,
                    "fall_detected": True,
                    "fall_severity": severity,
                    "status": random.choice(['pending', 'reviewed', 'resolved']),
                    "heart_rate": min(140, base_reading["heart_rate"] + severity*5 + random.randint(5,10)),
                    "spo2": max(80, base_reading["spo2"] - severity - random.randint(1,3)),
                    "temperature": base_reading["temperature"] + round(severity * 0.1, 1)
                }
                print(f"⚠️ Fall detected for {mrn} | Severity: {severity} | Status: {reading['status']}")
            else:
                reading = base_reading

            try:
                mqtt_service.client.publish(f"{topic_prefix}/{mrn}/readings", json.dumps(reading), qos=1)
                print(f"📤 Published to {topic_prefix}/{mrn}/readings")
            except Exception as e:
                print(f"⚠️ Publish failed: {e}. Will retry in next loop.")

        print(f"=== Batch completed at {datetime.now().strftime('%H:%M:%S')} ===\n")
        time.sleep(60)



if __name__ == "__main__":
    simulate_readings()