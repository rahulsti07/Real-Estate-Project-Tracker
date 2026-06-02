#!/usr/bin/env python
"""Test script to verify car sales analyzer module"""

import sys
sys.path.insert(0, 'c:\\Users\\Rahul\\Project Tracker')

from src.car_sales_analyzer import CarSalesAnalyzer

# Load and test the analyzer
analyzer = CarSalesAnalyzer('data/car_sales_india.csv')

# Calculate YoY growth
analyzer.calculate_yoy_growth()
print("✅ YoY growth calculated successfully")

# Get statistics
stats = analyzer.get_summary_stats()
print("\n📊 Fuel Type Summary (2026):")
print("-" * 60)

for fuel, data in stats.items():
    print(f"\n{fuel}:")
    print(f"  Current Sales: {data['current_sales']:,} units")
    print(f"  Avg YoY Growth: {data['avg_yoy']:.2f}%")
    print(f"  Total Growth (since 2015): {data['total_growth']:.2f}%")
    print(f"  YoY Range: {data['min_yoy']:.2f}% to {data['max_yoy']:.2f}%")

# Test forecasting
print("\n" + "=" * 60)
print("🔮 Testing 3-Year Forecast")
print("=" * 60)

for fuel in ["Petrol", "Diesel", "EV", "Hybrid"]:
    forecast = analyzer.forecast_trend(fuel, years_ahead=3)
    print(f"\n{fuel}:")
    for year, value in zip(forecast['years'], forecast['values']):
        print(f"  {int(year)}: {int(value):,} units")
    print(f"  Trend (units/year): {forecast['slope']:,.0f}")

# Test deviation detection
print("\n" + "=" * 60)
print("🚨 Deviation Analysis (>30%)")
print("=" * 60)

deviations = analyzer.detect_deviations()
has_deviations = False

for fuel, flagged in deviations.items():
    if flagged:
        has_deviations = True
        print(f"\n{fuel}:")
        for record in flagged:
            print(f"  Year {int(record['Year'])}: {record[f'{fuel}_YoY']:+.2f}%")

if not has_deviations:
    print("\n✅ No critical deviations detected (>30%)")

print("\n" + "=" * 60)
print("✅ All tests passed successfully!")
print("=" * 60)
