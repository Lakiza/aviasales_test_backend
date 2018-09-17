from flask import Flask, jsonify
from dashboard import DashboardData
from errors import Errors
import json

app = Flask(__name__)
file = open('dashboard_data.json', 'r')
dashboardData = DashboardData(file.read())

@app.route('/getMetrics/<period>', methods=['GET'])
def index(period):
    data = dashboardData.getDataForPeriod(period)
    if data is not None:
        data = data.copy()
        data['statisticAverage'] = dashboardData.getStatisticAverage()
        return jsonify({
            'type': 'success',
            'data': data
        })
    else: 
        return jsonify({
            'type':'error',
            'message': 'Undefined period', 
            'code': Errors.UNDEFINED_PERIOD
        })

if __name__ == '__main__':    
    app.run(debug=True)