from flask import Flask, render_template, request
import datetime
import mysql.connector

app = Flask(__name__)

def calculate_car_rate(duration):
    hours, minutes = divmod(duration, 60)
    if hours <= 2:
        rate = 50
    else:
        rate = 50 + ((hours - 2) * 10) + (minutes // 1 * 10)
    return rate

def calculate_motor_rate(duration):
    return 30

def calculate_employee_rate(duration):
    hours, minutes = divmod(duration, 60)
    total_rate = calculate_car_rate(duration)
    discount = 0.2 * total_rate
    rate = max(total_rate - discount, 0)
    return rate

@app.route('/')
def index():
    cnx = mysql.connector.connect(user='root', password='', host='localhost', database='data')

    cursor = cnx.cursor()

    cursor.execute("SELECT VehicleType, StartTime, EndTime, Cost FROM transactions")

    results = cursor.fetchall()

    return render_template('index.html', data = results)


@app.route('/calculate', methods=['POST'])
def calculate():
    vehicle_type = request.form['vehicle_type']
    start_time_str = request.form['start_time']
    end_time_str = request.form['end_time']

    start_time = datetime.datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M')
    end_time = datetime.datetime.strptime(end_time_str, '%Y-%m-%dT%H:%M')

    duration = (end_time - start_time).total_seconds() // 60
    hours = (end_time - start_time) / datetime.timedelta(hours=1)

    if vehicle_type == 'car':
        rate = calculate_car_rate(duration)
    elif vehicle_type == 'motor':
        rate = calculate_motor_rate(duration)
    elif vehicle_type == 'employee':
        rate = calculate_employee_rate(duration)
    
    return render_template('result.html', rate=rate, duration = hours)

if __name__ == '__main__':
    app.run(debug=True)
