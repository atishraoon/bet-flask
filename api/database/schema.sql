CREATE TABLE IF NOT EXISTS rounds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Time_slote TEXT NOT NULL,
    level_difficulty TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS rounds_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    round_id INTEGER NOT NULL,
    time_slot TEXT NOT NULL,
    r_one_ma INTEGER,
    r_one_et TEXT,
    r_one_hw INTEGER,
    r_two_ma INTEGER,
    r_two_et TEXT,
    r_two_st TEXT,
    r_two_hw INTEGER,
    r_three_ma INTEGER,
    r_three_et TEXT,
    r_three_st TEXT,
    r_three_hw INTEGER,
    pause_time TEXT,
    FOREIGN KEY (round_id) REFERENCES rounds(id) ON DELETE CASCADE
);