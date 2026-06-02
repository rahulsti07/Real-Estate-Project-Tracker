"""
Car Sales Analyzer Module
Analyzes year-on-year growth, forecasts trends, and flags deviations for Indian car sales data
"""

import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.linear_model import LinearRegression


class CarSalesAnalyzer:
    """Analyzes Indian car sales data with forecasting and deviation detection"""
    
    FUEL_TYPES = ["Petrol", "Diesel", "EV", "Hybrid"]
    DEVIATION_THRESHOLD = 30  # 30% threshold
    
    def __init__(self, filepath):
        """Initialize with CSV data"""
        self.data = pd.read_csv(filepath)
        self.data['Year'] = self.data['Year'].astype(int)
        self.forecasts = {}
        self.deviations = {}
    
    def calculate_yoy_growth(self):
        """Calculate year-on-year growth percentage"""
        for col in self.FUEL_TYPES:
            self.data[f"{col}_YoY"] = self.data[col].pct_change() * 100
        return self.data[["Year", "Petrol_YoY", "Diesel_YoY", "EV_YoY", "Hybrid_YoY"]]
    
    def forecast_trend(self, fuel_type, years_ahead=3):
        """
        Forecast future sales using linear regression
        
        Args:
            fuel_type: One of ["Petrol", "Diesel", "EV", "Hybrid"]
            years_ahead: Number of years to forecast (default 3)
        
        Returns:
            Dictionary with forecasted values
        """
        X = self.data[["Year"]].values
        y = self.data[fuel_type].values
        
        model = LinearRegression()
        model.fit(X, y)
        
        last_year = self.data["Year"].max()
        forecast_years = np.array([[last_year + i] for i in range(1, years_ahead + 1)])
        forecasted_values = model.predict(forecast_years)
        
        self.forecasts[fuel_type] = {
            'years': forecast_years.flatten().tolist(),
            'values': forecasted_values.tolist(),
            'slope': float(model.coef_[0])
        }
        
        return self.forecasts[fuel_type]
    
    def detect_deviations(self):
        """
        Detect when actual YoY growth deviates significantly from expected trend
        Flags deviations > 30% as anomalies
        """
        for col in self.FUEL_TYPES:
            self.data[f"{col}_Deviation_Flag"] = (
                self.data[f"{col}_YoY"].abs() > self.DEVIATION_THRESHOLD
            )
        
        deviations_summary = {}
        for col in self.FUEL_TYPES:
            flagged = self.data[self.data[f"{col}_Deviation_Flag"] == True][
                ["Year", f"{col}_YoY"]
            ]
            deviations_summary[col] = flagged.to_dict('records')
        
        self.deviations = deviations_summary
        return deviations_summary
    
    def get_summary_stats(self):
        """Get summary statistics for each fuel type"""
        stats = {}
        for col in self.FUEL_TYPES:
            stats[col] = {
                'current_year': int(self.data['Year'].max()),
                'current_sales': int(self.data[col].iloc[-1]),
                'avg_yoy': round(self.data[f"{col}_YoY"].mean(), 2),
                'max_yoy': round(self.data[f"{col}_YoY"].max(), 2),
                'min_yoy': round(self.data[f"{col}_YoY"].min(), 2),
                'total_growth': round(
                    ((self.data[col].iloc[-1] - self.data[col].iloc[0]) / self.data[col].iloc[0]) * 100, 
                    2
                )
            }
        return stats
    
    def get_full_analysis(self, years_ahead=3):
        """Generate complete analysis"""
        return {
            'yoy_growth': self.calculate_yoy_growth(),
            'deviations': self.detect_deviations(),
            'forecasts': {
                fuel: self.forecast_trend(fuel, years_ahead) 
                for fuel in self.FUEL_TYPES
            },
            'summary_stats': self.get_summary_stats()
        }
