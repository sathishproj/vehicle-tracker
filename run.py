from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/vehicles")
def vehicles():
    return render_template("vehicles.html")


@app.route("/tracking")
def tracking():
    return render_template("live_tracking.html")


@app.route("/geofence")
def geofence():
    return render_template("geofence.html")


@app.route("/reports")
def reports():
    return render_template("reports.html")


if __name__ == "__main__":
    app.run(debug=True)