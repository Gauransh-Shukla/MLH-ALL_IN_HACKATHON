import sqlite3
import pandas as pd

# Database Functions
def create_db():
    conn = sqlite3.connect('cbt_app.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS thought_record
                 (situation TEXT, feeling TEXT, thought TEXT, evidence_for TEXT, evidence_against TEXT, alternative_thought TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS goals (goal TEXT)''')
    conn.close()

def insert_into_db(situation, feeling, thought, evidence_for, evidence_against, alternative_thought):
    conn = sqlite3.connect('cbt_app.db')
    c = conn.cursor()
    c.execute("INSERT INTO thought_record (situation, feeling, thought, evidence_for, evidence_against, alternative_thought) VALUES (?, ?, ?, ?, ?, ?)",
              (situation, feeling, thought, evidence_for, evidence_against, alternative_thought))
    conn.commit()
    conn.close()

def insert_goal(goal):
    conn = sqlite3.connect('cbt_app.db')
    c = conn.cursor()
    c.execute("INSERT INTO goals (goal) VALUES (?)", (goal,))
    conn.commit()
    conn.close()

def get_goals():
    conn = sqlite3.connect('cbt_app.db')
    df = pd.read_sql_query("SELECT * FROM goals", conn)
    return df['goal'].tolist()
