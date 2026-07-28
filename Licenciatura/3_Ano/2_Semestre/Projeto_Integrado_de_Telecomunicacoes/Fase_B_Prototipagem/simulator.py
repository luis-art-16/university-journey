import paho.mqtt.client as mqtt
import json
import random
from datetime import datetime
import time
from app import create_app
from app.services.database_service import get_db_session
from app.models import Patient

app = create_app()
broker = "localhost"
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
            return [patient.patient_id for patient in patients]
        finally:
            db_session.close()

def generate_fall_reading(base_values):
    """Generate realistic fall data with severity levels"""
    severity = random.choices(
        [1, 2, 3, 4, 5],
        weights=[35, 30, 20, 10, 5],  # Probability distribution
        k=1
    )[0]
    
    return {
        **base_values,
        "fall_detected": True,
        "fall_severity": severity,
        "heart_rate": min(140, base_values["heart_rate"] + severity * 5 + random.randint(5, 10)),
        "spo2": max(80, base_values["spo2"] - severity - random.randint(1, 3)),
        "temperature": base_values["temperature"] + round(severity * 0.1, 1)
    }

def simulate_readings():
    client = mqtt.Client()
    client.connect(broker, port)
    
    patient_ids = get_all_patient_ids()
    
    if not patient_ids:
        print("No patients found in database!")
        return
    
    while True:
        timestamp = datetime.now().isoformat()
        
        for patient_id in patient_ids:
            # Base vital signs
            base_reading = {
                "timestamp": timestamp,
                "heart_rate": generate_heart_rate(),
                "spo2": generate_spo2(),
                "temperature": generate_temperature(),
                "fall_detected": False,
                "fall_severity": None
            }
            
            # 5% chance of fall
            if random.random() < 0.05:
                reading = generate_fall_reading(base_reading)
                print(f"⚠️ Fall detected for {patient_id} (Severity {reading['fall_severity']})")
            else:
                reading = base_reading
            
            topic = f"{topic_prefix}/{patient_id}/readings"
            client.publish(topic, json.dumps(reading), qos=1)
            print(f"Published to {topic}: {json.dumps(reading, indent=2)}")
        
        print(f"=== Batch completed at {datetime.now().strftime('%H:%M:%S')} ===")
        time.sleep(60)  # 10-second intervals between batches

if __name__ == "__main__":
    simulate_readings()