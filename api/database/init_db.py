import sqlite3
from contextlib import contextmanager

DATABASE_FILE = 'database.db'

def init_db():
    """Initialize the database by creating tables from schema.sql"""
    with db_connection() as conn:
        with open('schema.sql', 'r') as f:
            schema_script = f.read()
        conn.executescript(schema_script)
        print("Database initialized with schema.sql")

def insert_sample_data():
    """Insert sample data into both rounds and rounds_info tables"""
    sample_rounds = [
        {
            "Time_slote": "10.00", 
            "level_difficulty": "easy",
            "rounds_info": {
                "time_slot": "10.00",
                
                "r_one_ma": 5,
                "r_one_et": "10.10",
                "r_one_hw": 2,
                
                "r_two_ma": 10,
                "r_two_et": "10.40",
                "r_two_st": "10.30",
                "r_two_hw": 3,
                
                "r_three_ma": 100,
                "r_three_et": "11.10",
                "r_three_st": "11.00",
                "r_three_hw": 5,
                
                "pause_time": "10"
            }
        }
    ]
    
    with db_connection() as conn:
        cursor = conn.cursor()
        
        for round_data in sample_rounds:
            # Insert into rounds table
            cursor.execute(
                "INSERT INTO rounds (Time_slote, level_difficulty) VALUES (?, ?)",
                (round_data["Time_slote"], round_data["level_difficulty"])
            )
            
            # Get the ID of the newly inserted round
            round_id = cursor.lastrowid
            
            # Insert into rounds_info table
            info_data = round_data["rounds_info"]
            cursor.execute(
                """INSERT INTO rounds_info (
                    round_id, time_slot, 
                    r_one_ma, r_one_et, r_one_hw,
                    r_two_ma, r_two_et, r_two_st, r_two_hw,
                    r_three_ma, r_three_et, r_three_st, r_three_hw,
                    pause_time
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    round_id, info_data["time_slot"],
                    info_data["r_one_ma"], info_data["r_one_et"], info_data["r_one_hw"],
                    info_data["r_two_ma"], info_data["r_two_et"], info_data["r_two_st"], info_data["r_two_hw"],
                    info_data["r_three_ma"], info_data["r_three_et"], info_data["r_three_st"], info_data["r_three_hw"],
                    info_data["pause_time"]
                )
            )
            
        conn.commit()
        print(f"Inserted {len(sample_rounds)} sample rounds with their associated info")

@contextmanager
def db_connection():
    """Context manager for database connections"""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def get_db_connection():
    """Get a database connection"""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def execute_query(query, args=(), one=False):
    """Execute a query and return results"""
    with db_connection() as conn:
        cursor = conn.execute(query, args)
        results = cursor.fetchall()
        conn.commit()
    return (results[0] if results else None) if one else results

if __name__ == '__main__':
    init_db()
    insert_sample_data()
    print("Database setup complete. Created database.db with sample rounds data.")