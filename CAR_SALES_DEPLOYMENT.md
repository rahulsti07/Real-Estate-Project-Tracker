# 🚗 Car Sales Analysis Agent - Deployment Guide

## ✅ Successfully Deployed to GitHub

**Repository:** https://github.com/rahulsti07/Real-Estate-Project-Tracker  
**Branch:** main  
**Latest Commit:** `48fdf70` - "Add Car Sales Analysis Agent with forecasting and deviation detection"

---

## 📦 What Was Deployed

### New Files
- ✅ `src/car_sales_analyzer.py` - Core analysis engine
- ✅ `pages/car_sales_analysis.py` - Streamlit dashboard page
- ✅ `data/car_sales_india.csv` - Sample data (2015-2026)
- ✅ `test_car_sales_analyzer.py` - Unit tests

### Updated Files
- ✅ `README.md` - Added Car Sales Agent documentation
- ✅ `requirements.txt` - Added scikit-learn dependency

---

## 🎯 Features Included

### Car Sales Analyzer Module
```python
from src.car_sales_analyzer import CarSalesAnalyzer

analyzer = CarSalesAnalyzer('data/car_sales_india.csv')
```

**Capabilities:**
- Year-on-Year growth calculations
- Linear regression forecasting (3+ years ahead)
- Automatic deviation detection (30% threshold)
- Multi-fuel type analysis (Petrol, Diesel, EV, Hybrid)
- Summary statistics and trend analysis

### Streamlit Dashboard
**Access:** Select "🚗 Car Sales Analysis" in sidebar

**Sections:**
1. **Summary Statistics** - Current sales, growth rates, ranges
2. **Sales Volume Comparison** - Bar charts by fuel type
3. **YoY Growth Trends** - Line chart with historical data
4. **Deviation Analysis** - Flags for >30% changes
5. **Sales Forecasts** - 2027-2029 predictions
6. **Market Share Evolution** - Pie charts for selected years

---

## 📊 Sample Data Overview

**Data File:** `data/car_sales_india.csv`

| Metric | Petrol | Diesel | EV | Hybrid |
|--------|--------|--------|-----|---------|
| 2026 Sales | 2.5M | 2.35M | 2.2M | 1.55M |
| Avg YoY | +4.5% | +6.6% | +75.8% | +62.5% |
| Total Growth | +60.3% | +95.8% | +43,900% | +19,275% |

---

## 🚀 Installation & Setup

### 1. Clone Repository
```bash
git clone https://github.com/rahulsti07/Real-Estate-Project-Tracker.git
cd "Project Tracker"
```

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Dashboard
```bash
streamlit run app.py
```

Navigate to http://localhost:8501 and select "Car Sales Analysis"

---

## 📋 File Structure

```
Project Tracker/
├── app.py                        # Main Streamlit app
├── pages/
│   └── car_sales_analysis.py    # 🆕 Car Sales Dashboard
├── src/
│   ├── car_sales_analyzer.py    # 🆕 Analysis Engine
│   ├── database.py
│   ├── variance_engine.py
│   └── utils.py
├── data/
│   ├── car_sales_india.csv      # 🆕 Sample Data
│   ├── projecttracker.db
│   ├── uploads/
│   └── exports/
├── requirements.txt              # 📝 Updated
├── README.md                     # 📝 Updated
└── test_car_sales_analyzer.py   # 🆕 Tests
```

---

## 🧪 Testing

Run the test script to verify installation:
```bash
python test_car_sales_analyzer.py
```

**Expected Output:**
```
✅ YoY growth calculated successfully
✅ All tests passed successfully!
```

---

## 🔧 Key Dependencies

```
streamlit==1.28.1       # Web dashboard
pandas==2.0.3           # Data manipulation
plotly==5.17.0          # Interactive charts
scikit-learn==1.3.2     # Linear regression forecasting
openpyxl==3.1.2         # Excel export
```

---

## 📈 Analysis Features

### Year-on-Year Growth
- Calculates percentage change year-over-year
- Identifies trends and anomalies
- Visualizes growth patterns

### Forecasting
- Uses linear regression for trend prediction
- Generates 3-year forecasts (2027-2029)
- Shows growth slope (units per year)

### Deviation Detection
- Flags changes exceeding 30% threshold
- Highlights critical market shifts
- Useful for trend analysis and alerts

### Market Share Analysis
- Visualizes fuel type distribution
- Shows evolution across years
- Pie charts for easy comparison

---

## 💡 Example Usage

```python
from src.car_sales_analyzer import CarSalesAnalyzer

# Load data
analyzer = CarSalesAnalyzer('data/car_sales_india.csv')

# Get statistics
stats = analyzer.get_summary_stats()
print(f"EV Sales 2026: {stats['EV']['current_sales']:,} units")
print(f"Avg EV Growth: {stats['EV']['avg_yoy']:.2f}%")

# Forecast
forecast = analyzer.forecast_trend('EV', years_ahead=3)
print(f"EV 2029 Forecast: {int(forecast['values'][-1]):,} units")

# Detect deviations
deviations = analyzer.detect_deviations()
if deviations['EV']:
    print(f"EV Critical Years: {len(deviations['EV'])} years flagged")
```

---

## 🎓 Documentation

- **Main README:** [README.md](README.md)
- **Deployment Guide:** [DEPLOYMENT.md](DEPLOYMENT.md)
- **Car Sales Analyzer Docstring:** `src/car_sales_analyzer.py`

---

## ✨ Future Enhancements

- [ ] Add more fuel types (Fuel Cell, Plug-in Hybrid)
- [ ] Implement ARIMA/Prophet forecasting
- [ ] Add comparison across regions
- [ ] Export forecasts to CSV
- [ ] Real-time data integration from APIs
- [ ] Advanced statistical analysis

---

## 📞 Support

For issues or questions:
1. Check `test_car_sales_analyzer.py` for examples
2. Review docstrings in `src/car_sales_analyzer.py`
3. See `pages/car_sales_analysis.py` for UI implementation

---

**Deployed:** June 2, 2026  
**Status:** ✅ Production Ready  
**Version:** 1.0.0
