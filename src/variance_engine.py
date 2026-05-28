"""Variance calculation engine for ProjectTracker"""

import pandas as pd
from datetime import datetime
from .database import log_variance


class VarianceAnalyzer:
    """Calculate and flag deviations between projected and actual values"""
    
    DEVIATION_THRESHOLD = 30  # 30% threshold for major deviations
    
    def __init__(self):
        self.results = []
    
    @staticmethod
    def calculate_variance(projected, actual):
        """Calculate variance (Actual - Projected)"""
        if projected == 0:
            return None
        return actual - projected
    
    @staticmethod
    def calculate_percent_deviation(variance, projected):
        """Calculate percentage deviation: (Variance / Projected) * 100"""
        if projected == 0:
            return None
        return (variance / projected) * 100
    
    @staticmethod
    def flag_deviation(percent_deviation):
        """Flag deviations > 30% as major"""
        if percent_deviation is None:
            return "N/A"
        
        abs_deviation = abs(percent_deviation)
        
        if abs_deviation > VarianceAnalyzer.DEVIATION_THRESHOLD:
            return f"🚨 Major Deviation ({percent_deviation:.2f}%)"
        else:
            return f"✅ OK ({percent_deviation:.2f}%)"
    
    def analyze_project(self, parameters_data):
        """
        Analyze variance for project parameters
        
        Args:
            parameters_data: List of tuples (name, projected, actual, unit)
        
        Returns:
            DataFrame with variance analysis
        """
        data = {
            "Parameter": [],
            "Projected": [],
            "Actual": [],
            "Unit": [],
            "Variance": [],
            "% Deviation": [],
            "Status": []
        }
        
        for param_name, projected, actual, unit, param_id in parameters_data:
            if actual is None:
                continue
            
            variance = self.calculate_variance(projected, actual)
            pct_deviation = self.calculate_percent_deviation(variance, projected)
            status = self.flag_deviation(pct_deviation)
            
            # Log to database
            log_variance(param_id, variance, pct_deviation, status)
            
            data["Parameter"].append(param_name)
            data["Projected"].append(projected)
            data["Actual"].append(actual)
            data["Unit"].append(unit)
            data["Variance"].append(variance)
            data["% Deviation"].append(pct_deviation)
            data["Status"].append(status)
        
        df = pd.DataFrame(data)
        
        # Format numeric columns
        if not df.empty:
            df["Variance"] = df["Variance"].round(2)
            df["% Deviation"] = df["% Deviation"].round(2)
        
        return df
    
    def get_flagged_parameters(self, df):
        """Extract only flagged major deviations"""
        if df.empty:
            return df
        return df[df["Status"].str.contains("Major Deviation", na=False)]
    
    def generate_summary(self, df):
        """Generate summary statistics"""
        if df.empty:
            return {
                "total_parameters": 0,
                "flagged_count": 0,
                "ok_count": 0,
                "avg_deviation": 0
            }
        
        flagged = df[df["Status"].str.contains("Major Deviation", na=False)]
        
        return {
            "total_parameters": len(df),
            "flagged_count": len(flagged),
            "ok_count": len(df) - len(flagged),
            "avg_deviation": df["% Deviation"].abs().mean()
        }
