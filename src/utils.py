"""Utility functions for ProjectTracker"""

import pandas as pd
import csv
from io import StringIO


def parse_csv(file_content):
    """Parse CSV file content into DataFrame"""
    try:
        df = pd.read_csv(StringIO(file_content))
        return df
    except Exception as e:
        return None


def validate_project_data(df):
    """Validate required columns in project data"""
    required_columns = ["Parameter", "Projected"]
    
    if not all(col in df.columns for col in required_columns):
        return False, f"Missing required columns: {required_columns}"
    
    # Check for valid numeric values
    try:
        df["Projected"] = pd.to_numeric(df["Projected"])
        if "Actual" in df.columns:
            df["Actual"] = pd.to_numeric(df["Actual"], errors="coerce")
    except Exception as e:
        return False, f"Invalid numeric values: {str(e)}"
    
    return True, "Valid"


def format_currency(value, currency="₹"):
    """Format value as currency"""
    if isinstance(value, (int, float)):
        return f"{currency} {value:,.2f}"
    return str(value)


def format_percentage(value):
    """Format value as percentage"""
    if isinstance(value, (int, float)):
        return f"{value:.2f}%"
    return str(value)
