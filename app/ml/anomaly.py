import numpy as np
from sklearn.ensemble import IsolationForest

def detect_anomaly(speed, latitude, longitude):
    data = np.array([[30,17.3850,78.4867],[45,17.3900,78.4900],[55,17.3950,78.5000],[60,17.3800,78.4700],[35,17.3700,78.4800],[50,17.4000,78.5100]])
    model = IsolationForest(contamination=0.20, random_state=42).fit(data)
    pred = model.predict([[speed, latitude, longitude]])[0]
    reasons = []
    if speed > 80: reasons.append('Overspeed detected')
    if pred == -1: reasons.append('Unusual GPS movement pattern detected')
    return bool(reasons), ', '.join(reasons) if reasons else 'Normal'
