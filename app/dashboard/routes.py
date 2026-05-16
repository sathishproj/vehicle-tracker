from flask import Blueprint, render_template
from flask_login import login_required
from app.models import Vehicle, TrackingLog, Alert, User

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def index():
    stats = {'vehicles':Vehicle.query.count(),'logs':TrackingLog.query.count(),'alerts':Alert.query.filter_by(status='Open').count(),'users':User.query.count()}
    latest_logs = TrackingLog.query.order_by(TrackingLog.timestamp.desc()).limit(10).all()
    alerts = Alert.query.order_by(Alert.timestamp.desc()).limit(10).all()
    return render_template('dashboard.html', stats=stats, latest_logs=latest_logs, alerts=alerts)
