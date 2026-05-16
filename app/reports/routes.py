from flask import Blueprint, render_template, request
from flask_login import login_required
from app.models import TrackingLog, Alert, Vehicle

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/', methods=['GET','POST'])
@login_required
def index():
    vehicles = Vehicle.query.all(); logs=[]; alerts=[]
    if request.method == 'POST':
        vehicle_id = request.form.get('vehicle_id')
        logs = TrackingLog.query.filter_by(vehicle_id=vehicle_id).order_by(TrackingLog.timestamp.desc()).all()
        alerts = Alert.query.filter_by(vehicle_id=vehicle_id).order_by(Alert.timestamp.desc()).all()
    return render_template('reports.html', vehicles=vehicles, logs=logs, alerts=alerts)
