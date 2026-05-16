from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models import GeoFence

geofence_bp = Blueprint('geofence', __name__)

@geofence_bp.route('/', methods=['GET','POST'])
@login_required
def index():
    if request.method == 'POST':
        fence = GeoFence(name=request.form.get('name'), center_lat=float(request.form.get('center_lat')), center_lng=float(request.form.get('center_lng')), radius_meters=float(request.form.get('radius_meters')))
        db.session.add(fence); db.session.commit(); flash('Geo-fence added successfully', 'success')
        return redirect(url_for('geofence.index'))
    return render_template('geofence.html', fences=GeoFence.query.all())
