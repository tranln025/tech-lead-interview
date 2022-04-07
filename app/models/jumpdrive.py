from app import db
from app.models import base_model
from sqlalchemy.orm import synonym


class jumpdrive_device(base_model):
    jumpdrive_device_id = db.Column(db.BigInteger, primary_key=True)
    id = synonym(jumpdrive_device_id)
    serial_number = db.Column(db.String(63), nullable=False)
    # Nullable true to allow users to register a device before it is paired or remove a vin if a customer returns the device
    vin = db.Column(db.String(63), nullable=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)


class jumpdrive_event(base_model):
    jumpdrive_event_id = db.Column(db.BigInteger, primary_key=True)
    id = synonym(jumpdrive_event_id)
    serial_number = db.Column(db.String(63), nullable=False)
    vin = db.Column(db.String(63), nullable=False)
    last_time_in = db.Column(db.Integer, nullable=False)
    fuel_percent = db.Column(db.Float, nullable=True)
    battery_level_mV = db.Column(db.Integer, nullable=True)
    odometer_km = db.Column(db.Float, nullable=True)
    # Data will be available in JumpDrive gen3
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)