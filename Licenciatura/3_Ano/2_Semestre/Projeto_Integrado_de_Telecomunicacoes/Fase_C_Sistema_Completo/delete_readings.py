from app import create_app, db
from app.models import PatientReading, FallEvent

def delete_all_patient_readings_and_falls():
    """
    Deletes all patient readings and fall events from the database
    """
    app = create_app()
    
    with app.app_context():
        try:
            # Delete all records from FallEvent table first (if there's a foreign key dependency)
            num_falls_deleted = db.session.query(FallEvent).delete()
            
            # Then delete all records from PatientReading table
            num_readings_deleted = db.session.query(PatientReading).delete()
            
            # Commit the transaction
            db.session.commit()
            
            print(f"Successfully deleted {num_readings_deleted} patient readings and {num_falls_deleted} fall events")
            
        except Exception as e:
            # Rollback in case of error
            db.session.rollback()
            print(f"Error deleting data: {str(e)}")
        finally:
            # Ensure session is closed
            db.session.close()

if __name__ == "__main__":
    delete_all_patient_readings_and_falls()
