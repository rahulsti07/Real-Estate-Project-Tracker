"""Database initialization and management for ProjectTracker"""

import sqlite3
import os
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "projecttracker.db"


def init_database():
    """Initialize SQLite database with required tables"""
    os.makedirs(DB_PATH.parent, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Projects table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            start_date TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Parameters table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS parameters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            parameter_name TEXT NOT NULL,
            projected_value REAL NOT NULL,
            actual_value REAL,
            unit TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (project_id) REFERENCES projects(id)
        )
    """)
    
    # Variance tracking table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS variance_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            parameter_id INTEGER NOT NULL,
            variance REAL,
            percent_deviation REAL,
            flag_status TEXT,
            recorded_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (parameter_id) REFERENCES parameters(id)
        )
    """)
    
    conn.commit()
    conn.close()


def get_connection():
    """Get database connection"""
    return sqlite3.connect(DB_PATH)


def get_all_projects():
    """Retrieve all projects"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, description, start_date FROM projects ORDER BY created_at DESC")
    projects = cursor.fetchall()
    conn.close()
    return projects


def get_project_parameters(project_id):
    """Get all parameters for a project"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, parameter_name, projected_value, actual_value, unit
        FROM parameters 
        WHERE project_id = ?
        ORDER BY created_at ASC
    """, (project_id,))
    params = cursor.fetchall()
    conn.close()
    return params


def add_project(name, description="", start_date=""):
    """Add new project"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO projects (name, description, start_date)
            VALUES (?, ?, ?)
        """, (name, description, start_date))
        conn.commit()
        project_id = cursor.lastrowid
        conn.close()
        return project_id
    except sqlite3.IntegrityError:
        conn.close()
        return None


def add_parameter(project_id, parameter_name, projected_value, unit=""):
    """Add parameter to project"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO parameters (project_id, parameter_name, projected_value, unit)
        VALUES (?, ?, ?, ?)
    """, (project_id, parameter_name, projected_value, unit))
    conn.commit()
    param_id = cursor.lastrowid
    conn.close()
    return param_id


def update_actual_value(parameter_id, actual_value):
    """Update actual value for a parameter"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE parameters SET actual_value = ? WHERE id = ?
    """, (actual_value, parameter_id))
    conn.commit()
    conn.close()


def log_variance(parameter_id, variance, percent_deviation, flag_status):
    """Log variance calculation"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO variance_log (parameter_id, variance, percent_deviation, flag_status)
        VALUES (?, ?, ?, ?)
    """, (parameter_id, variance, percent_deviation, flag_status))
    conn.commit()
    conn.close()


# Initialize database on module import
init_database()
