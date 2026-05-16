from app import create_app, db
from app.models import User, Driver, Vehicle, GeoFence
from werkzeug.security import generate_password_hash

app = create_app()

def seed():
    if not User.query.filter_by(email='admin@example.com').first():
        admin = User(name='Admin', email='admin@example.com', role='admin', password_hash=generate_password_hash('admin123'))
        driver = Driver(name='Ramesh', phone='9876543210', license_no='DL-TS-2026-1001')
        vehicle = Vehicle(vehicle_no='TS09AB1234', vehicle_type='School Bus', status='Active', driver=driver)
        fence = GeoFence(name='Hyderabad Operating Zone', center_lat=17.3850, center_lng=78.4867, radius_meters=12000)
        db.session.add_all([admin, driver, vehicle, fence])
        db.session.commit()

@app.cli.command('init-db')
def init_db():
    db.drop_all(); db.create_all(); seed(); print('Database initialized')

if __name__ == '__main__':
    with app.app_context():
        db.create_all(); seed()
    app.run(debug=True)
