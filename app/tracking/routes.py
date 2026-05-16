from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from app import db
from app.models import Vehicle, Driver, TrackingLog, Alert, GeoFence
from app.ml.anomaly import detect_anomaly
from app.utils import distance_meters

tracking_bp = Blueprint('tracking', __name__)

@tracking_bp.route('/vehicles', methods=['GET','POST'])
@login_required
def vehicles():
    if request.method == 'POST':
        driver = Driver.query.filter_by(name=request.form.get('driver_name')).first() or Driver(name=request.form.get('driver_name'), phone=request.form.get('phone'), license_no=request.form.get('license_no'))
        db.session.add(driver); db.session.flush()
        vehicle = Vehicle(vehicle_no=request.form.get('vehicle_no'), vehicle_type=request.form.get('vehicle_type'), status=request.form.get('status'), driver=driver)
        db.session.add(vehicle); db.session.commit(); flash('Vehicle registered successfully', 'success')
        return redirect(url_for('tracking.vehicles'))
    return render_template('vehicles.html', vehicles=Vehicle.query.all())

@tracking_bp.route('/live', methods=['GET','POST'])
@login_required
def live_tracking():
    vehicles = Vehicle.query.all()
    if request.method == 'POST':
        vehicle_id = int(request.form.get('vehicle_id'))
        lat = float(request.form.get('latitude')); lng = float(request.form.get('longitude')); speed = float(request.form.get('speed'))
        anomaly, reason = detect_anomaly(speed, lat, lng)
        log = TrackingLog(vehicle_id=vehicle_id, latitude=lat, longitude=lng, speed=speed, location=request.form.get('location'), is_anomaly=anomaly, anomaly_reason=reason)
        db.session.add(log)
        if anomaly: db.session.add(Alert(vehicle_id=vehicle_id, alert_type='ANOMALY', message=reason))
        for fence in GeoFence.query.all():
            dist = distance_meters(fence.center_lat, fence.center_lng, lat, lng)
            if dist > fence.radius_meters:
                db.session.add(Alert(vehicle_id=vehicle_id, alert_type='GEOFENCE', message=f'Vehicle moved outside {fence.name}. Distance: {round(dist)} meters'))
        db.session.commit(); flash('Tracking data submitted successfully', 'success')
        return redirect(url_for('tracking.live_tracking'))
    latest = TrackingLog.query.order_by(TrackingLog.timestamp.desc()).limit(15).all()
    return render_template('live_tracking.html', vehicles=vehicles, latest=latest)

@tracking_bp.route('/api/latest')
def api_latest():
    logs = TrackingLog.query.order_by(TrackingLog.timestamp.desc()).limit(10).all()
    return jsonify([{'vehicle':l.vehicle.vehicle_no,'lat':l.latitude,'lng':l.longitude,'speed':l.speed,'location':l.location,'anomaly':l.is_anomaly,'time':l.timestamp.isoformat()} for l in logs])
