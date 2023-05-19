from flask import Flask, render_template, request
import csv
from datetime import datetime

app = Flask(__name__)

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for handling form submission
@app.route('/simulate', methods=['POST'])
def simulate():
    start_date = datetime.strptime(request.form['start_date'], "%Y-%m-%d").date()
    end_date = datetime.strptime(request.form['end_date'], "%Y-%m-%d").date()
    money_invested = float(request.form['money_invested'])

    # Read the CSV file
    data = []
    with open('data/s&p500_data.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            date = datetime.strptime(row['Date'], "%Y-%m-%d").date()
            if start_date <= date <= end_date:
                data.append({
                    'date': date,
                    'open': float(row['Open']),
                    'close': float(row['Close'])
                })

    # Perform the simulation trading logic
    portfolio_value = money_invested
    trades = 0
    for i in range(len(data) - 1):
        current_price = data[i]['close']
        next_price = data[i + 1]['open']
        if next_price > current_price:
            # Buy
            shares_to_buy = portfolio_value / current_price
            portfolio_value = shares_to_buy * next_price
            trades += 1

    # Convert portfolio value to a dollar amount with 2 decimal places
    portfolio_value = round(portfolio_value, 2)

    # Calculate the percentage change
    percent_change = ((portfolio_value - money_invested) / money_invested) * 100

    # Calculate the current value
    current_value = portfolio_value

    # Construct the simulation result
    simulation_result = {
        'start_date': start_date,
        'end_date': end_date,
        'money_invested': money_invested,
        'portfolio_value': portfolio_value,
        'trades': trades,
        'percent_change': percent_change,
        'current_value': current_value
    }

    return render_template('result.html', result=simulation_result)

if __name__ == '__main__':
    app.run(debug=True)
