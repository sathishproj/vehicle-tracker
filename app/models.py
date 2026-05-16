from datetime import datetime
from flask_login import UserMixin
from app import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user')

class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    license_no = db.Column(db.String(50))
    vehicles = db.relationship('Vehicle', backref='driver', lazy=True)

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_no = db.Column(db.String(30), unique=True, nullable=False)
    vehicle_type = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(30), default='Active')
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'))
    logs = db.relationship('TrackingLog', backref='vehicle', lazy=True)

class TrackingLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    speed = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(150))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    is_anomaly = db.Column(db.Boolean, default=False)
    anomaly_reason = db.Column(db.String(200))

class GeoFence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    center_lat = db.Column(db.Float, nullable=False)
    center_lng = db.Column(db.Float, nullable=False)
    radius_meters = db.Column(db.Float, nullable=False)

class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)
    alert_type = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(30), default='Open')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
