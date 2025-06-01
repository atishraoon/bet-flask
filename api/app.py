from flask import Flask, jsonify, request, render_template
import sqlite3
import os


from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Alternatively, you can enable CORS for specific routes only:
# CORS(app, resources={r"/api/*": {"origins": "http://localhost:8000"}})
app.config['JSON_SORT_KEYS'] = False
DATABASE = os.path.join('database', 'database.db')

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn



@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://127.0.0.1:8000')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


# --------------------------------------- home -----------------------------------

@app.route('/')
def home():   
    return jsonify({"message": "you are now allowed here"})

# -------------------------------- display all slotes-----------------------------------

@app.route('/api/rounds')
def show_rounds():
    conn = get_db_connection()
    rounds = conn.execute('SELECT * FROM rounds ORDER BY id').fetchall()
    conn.close()
    
    rounds_list = []
    for row in rounds:
        rounds_list.append({
            'id': row['id'],
            'Time_slote': row['Time_slote'],
            'level_difficulty': row['level_difficulty'].lower()
        })
    
    return jsonify({
        'count': len(rounds_list),
        'rounds': rounds_list
    })


# --------------------------- post time slotes ----------------------------------------

@app.route('/api/rounds-add', methods=['GET', 'POST'])
def add_round():
    if request.method == 'GET':
        return render_template('form/add-ts.html')
    
    # Handle POST request
    time_slote = request.form.get('time_slote')
    level_difficulty = request.form.get('level_difficulty')
    
    if not time_slote or not level_difficulty:
        return render_template('form/add-ts.html', 
                             message="Both fields are required",
                             success=False)
    
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO rounds (Time_slote, level_difficulty) VALUES (?, ?)",
            (time_slote, level_difficulty)
        )
        conn.commit()
        return render_template('form/add-ts.html', 
                            message="Round added successfully!",
                            success=True)
    except sqlite3.Error as e:
        return render_template('form/add-ts.html', 
                            message=f"Error: {str(e)}",
                            success=False)
    finally:
        conn.close()


# ------------------------------ display slots details ---------------------------------


@app.route('/api/rounds/<time_slot>')
def get_round_details(time_slot):
    conn = get_db_connection()
    
    try:
        # Get the basic round info
        round_data = conn.execute(
            'SELECT * FROM rounds WHERE Time_slote = ?', 
            (time_slot,)
        ).fetchone()
        
        if not round_data:
            return jsonify({"error": "Time slot not found"}), 404
        
        # Get the detailed info from rounds_info
        round_info = conn.execute(
            '''SELECT * FROM rounds_info 
               WHERE round_id = ?''',
            (round_data['id'],)
        ).fetchone()
        
        if not round_info:
            return jsonify({"error": "No details found for this time slot"}), 404
        
        # Combine the data into a single response
        response = {
            "time_slot": round_data['Time_slote'],
            "level_difficulty": round_data['level_difficulty'],
            "details": {
                "round_one": {
                    "min_amount": round_info['r_one_ma'],
                    "round_one_et": round_info['r_one_et'],
                    "round_one_hw": round_info['r_one_hw']
                },
                "round_two": {
                    "min_amount": round_info['r_two_ma'],
                    "round_two_et": round_info['r_two_et'],
                    "round_two_st": round_info['r_two_st'],
                    "round_two_hw": round_info['r_two_hw']
                },
                "round_three": {
                    "min_amount": round_info['r_three_ma'],
                    "round_three_et": round_info['r_three_et'],
                    "round_three_st": round_info['r_three_st'],
                    "round_three_hw": round_info['r_three_hw']
                },
                "pause_time": round_info['pause_time']
            }
        }
        
        return jsonify(response)
        
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()




# ----------------------------------- add slot info -------------------------------


@app.route('/api/rounds/add-full', methods=['GET', 'POST'])
def add_full_round():
    if request.method == 'GET':
        return render_template('form/ts-info.html')
    
    # Handle POST request 
    try:
        # Get all form data
        time_slote = request.form['time_slote']
        level_difficulty = request.form['level_difficulty']
        
        # Round info data
        rounds_info = {
            'time_slot': time_slote,
            'r_one_ma': request.form['r_one_ma'],
            'r_one_et': request.form['r_one_et'],
            'r_one_hw': request.form['r_one_hw'],
            'r_two_ma': request.form['r_two_ma'],
            'r_two_et': request.form['r_two_et'],
            'r_two_st': request.form['r_two_st'],
            'r_two_hw': request.form['r_two_hw'],
            'r_three_ma': request.form['r_three_ma'],
            'r_three_et': request.form['r_three_et'],
            'r_three_st': request.form['r_three_st'],
            'r_three_hw': request.form['r_three_hw'],
            'pause_time': request.form['pause_time']
        }

        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Insert into rounds table
        cursor.execute(
            "INSERT INTO rounds (Time_slote, level_difficulty) VALUES (?, ?)",
            (time_slote, level_difficulty)
        )
        
        # Get the ID of the newly inserted round
        round_id = cursor.lastrowid
        
        # Insert into rounds_info table
        cursor.execute(
            """INSERT INTO rounds_info (
                round_id, time_slot, 
                r_one_ma, r_one_et, r_one_hw,
                r_two_ma, r_two_et, r_two_st, r_two_hw,
                r_three_ma, r_three_et, r_three_st, r_three_hw,
                pause_time
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                round_id, rounds_info['time_slot'],
                rounds_info['r_one_ma'], rounds_info['r_one_et'], rounds_info['r_one_hw'],
                rounds_info['r_two_ma'], rounds_info['r_two_et'], rounds_info['r_two_st'], rounds_info['r_two_hw'],
                rounds_info['r_three_ma'], rounds_info['r_three_et'], rounds_info['r_three_st'], rounds_info['r_three_hw'],
                rounds_info['pause_time']
            )
        )
        
        conn.commit()
        return render_template('form/ts-info.html', 
                            message="Round information added successfully!",
                            success=True)
        
    except Exception as e:
        return render_template('form/ts-info.html', 
                            message=f"Error: {str(e)}",
                            success=False)
    finally:
        conn.close()



 
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)