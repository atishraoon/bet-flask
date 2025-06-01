from flask import Flask, jsonify, request, render_template
import requests  
import random

app = Flask(__name__)

# --------------------------------------- home -----------------------------------

@app.route('/')
def home():
    try:
        # Fetch data from the API
        response = requests.get('http://127.0.0.1:5000/api/rounds')
        response.raise_for_status()  
        rounds_data = response.json()

        
        return render_template('base/index.html', 
                             message="Round added successfully!",
                             success=True,
                             rounds_data=rounds_data)
    except requests.exceptions.RequestException as e:
        # Handle API request errors
        return render_template('base/index.html', 
                             message=f"Error fetching data: {str(e)}",
                             success=False,
                             rounds_data=[])

@app.route('/game/<time_slot>')
def game(time_slot):

    horse_win = random.randint(1, 5)
    try:
        response = requests.get(f'http://127.0.0.1:5000/api/rounds/{time_slot}')
        response.raise_for_status()
        round_data = response.json()  # Changed from rounds_data to round_data
        
        return render_template('base/game.html', 
                            message="Round details loaded successfully!",
                            success=True,
                            round_data=round_data,
                            horse_win=horse_win)  # Changed parameter name
    except requests.exceptions.RequestException as e:
        return render_template('base/game.html', 
                            message=f"Error fetching round details: {str(e)}",
                            success=False,
                            round_data=None)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)