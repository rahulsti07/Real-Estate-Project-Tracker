# 📊 ProjectTracker - Real Estate Variance Analysis System

A comprehensive dashboard for monitoring **Projected vs Actual** parameters in real estate projects with intelligent deviation flagging.

## 🎯 Features

✅ **Variance Analysis with 30% Deviation Flagging**
- Automatic calculation of variance and percentage deviation
- Flags major deviations (>30%) for immediate attention
- Visual indicators for quick status assessment

✅ **Project Management**
- Create and manage multiple real estate projects
- Add custom parameters per project
- Track projected and actual values

✅ **Data Import & Export**
- CSV upload functionality for batch parameter import
- Export analysis results to CSV and Excel formats
- Sample data included for quick testing

✅ **Interactive Dashboard**
- Real-time variance calculations
- Visual charts (Projected vs Actual, Deviation Analysis)
- Sortable and filterable parameter views
- Summary metrics and statistics

✅ **SQLite Database**
- Persistent project storage
- Variance history tracking
- Complete audit trail

✅ **Car Sales Analysis Module** 🚗
- Year-on-Year growth analysis for Indian car sales
- Forecasting with linear regression (3+ years ahead)
- Fuel type tracking: Petrol, Diesel, EV, Hybrid
- Market share visualization and trend analysis
- Automatic deviation flagging (>30% threshold)
- Interactive Streamlit dashboard with multi-year comparisons

---

## 📋 Project Structure

```
Project Tracker/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── src/
│   ├── __init__.py       # Package init
│   ├── database.py       # SQLite database management
│   ├── variance_engine.py # Variance calculation logic
│   ├── car_sales_analyzer.py  # Car sales analysis engine
│   └── utils.py          # Utility functions
├── pages/
│   └── car_sales_analysis.py  # Car sales dashboard (Streamlit page)
├── data/
│   ├── projecttracker.db # SQLite database (auto-created)
│   ├── car_sales_india.csv    # Indian car sales data
│   ├── sample_project.csv # Sample data
│   ├── uploads/          # CSV upload directory
│   └── exports/          # Export directory
└── .github/
    └── copilot-instructions.md
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Navigate to project directory:**
   ```bash
   cd "Project Tracker"
   ```

2. **Create virtual environment (recommended):**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment:**
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application:**
   ```bash
   streamlit run app.py
   ```

The app will open in your default browser at `http://localhost:8501`

---

## 📖 How to Use

### ⚠️ Important: Currency Specification
**All financial values must be entered in Indian Rupees (₹)**
- Use units like: `₹ Crore` (10 Million), `₹ Lakh` (100,000), or `₹` (Rupees)
- DO NOT use USD, $, or any other currency
- The system will display all values with ₹ symbol

### 1️⃣ Create a Project
- Click **"Create Project"** in the sidebar
- Enter project name, description, and start date
- Click **Create Project**

### 2️⃣ Add Parameters (Manual)
- Go to **"Add Parameters"** tab
- Enter parameter name, projected value, unit, and actual value
- Click **Add Parameter**
- Update actual values as they become available

### 3️⃣ Import from CSV
- Go to **"Upload CSV"** tab
- Prepare a CSV with columns: `Parameter`, `Projected`, `Actual` (optional), `Unit` (optional)
- Upload the file and click **Import Data into Project**

### 4️⃣ View Analysis
- Go to **"Dashboard"** tab
- See all parameters with variance calculations
- Major deviations (>30%) are highlighted with 🚨 flag
- View comparative charts and statistics

### 5️⃣ Export Results
- In Dashboard tab, use **Download CSV** or **Download Excel** buttons
- Results include all variance calculations

### 🚗 Car Sales Analysis Dashboard
- Access via **"Car Sales Analysis"** page in the sidebar
- View year-on-year growth trends for Petrol, Diesel, EV, and Hybrid vehicles
- Analyze market share evolution and fuel type trends
- Review forecasts for 2027-2029 with linear regression analysis
- Identify critical deviations (>30%) automatically
- Interactive charts and detailed statistics

---

## 🎬 Demo Walkthrough

### Quick Demo Scenario
Here's what a typical workflow looks like:

**Step 1: Create a Project**
```
1. Click "Create Project" → Enter "Mumbai Tower A"
2. Add description and date → Submit
✓ Project created and ready for data
```

**Step 2: Add Parameters**
```
1. Go to "Add Parameters" tab
2. Add "Budget" → Projected: 50 Cr | Actual: 65 Cr
3. Add "Completion Time" → Projected: 12 months | Actual: 14 months
✓ Parameters saved to database
```

**Step 3: View Deviations**
```
1. Navigate to Dashboard → Variance Analysis table
2. Budget shows 🚨 (30% deviation - Major Alert)
3. Completion Time shows ✅ (16.67% - Within limits)
✓ Visual chart highlights variances instantly
```

### ⚠️ Important: Currency Specification
**All financial values must be entered in Indian Rupees (₹)**
- Use units like: `₹ Crore` (10 Million), `₹ Lakh` (100,000), or `₹` (Rupees)
- DO NOT use USD, $, or any other currency
- The system will display all values with ₹ symbol
- **Conversion Reference:**
  - 1 Crore = 10,000,000 (Ten Million Rupees)
  - 1 Lakh = 100,000 (One Hundred Thousand Rupees)
  - 1 Crore = 100 Lakhs

---

## 📊 Variance Calculation Formula

### Variance
```
Variance = Actual - Projected
```

### % Deviation
```
% Deviation = (Variance / Projected) × 100
```

### Flagging Rule
```
IF |% Deviation| > 30% → 🚨 Major Deviation
ELSE → ✅ OK
```

---

## 📁 Sample Data

A sample CSV file is included at `data/sample_project.csv`:

| Parameter | Projected | Actual | Unit |
|-----------|-----------|--------|------|
| Completion Time | 12 | 14 | months |
| Budget | 50 | 65 | ₹ Cr |
| Units Sold | 200 | 120 | units |
| Cost per Unit | 25 | 32 | ₹ Lakh |

**Result:** 
- Budget: 30% deviation ✓ (Flagged)
- Units Sold: -40% deviation ✓ (Flagged)
- Completion Time: 16.67% deviation ✓ (OK)
- Cost per Unit: 28% deviation ✓ (OK)

---

## 🗄️ Database Schema

### projects
- `id` - Project ID
- `name` - Project name (unique)
- `description` - Project description
- `start_date` - Project start date
- `created_at` - Record creation timestamp

### parameters
- `id` - Parameter ID
- `project_id` - Reference to project
- `parameter_name` - Parameter name
- `projected_value` - Projected value
- `actual_value` - Actual value (nullable)
- `unit` - Measurement unit
- `created_at` - Record creation timestamp

### variance_log
- `id` - Log ID
- `parameter_id` - Reference to parameter
- `variance` - Calculated variance
- `percent_deviation` - Percentage deviation
- `flag_status` - Deviation flag status
- `recorded_at` - Recording timestamp

---

## 🔧 Configuration

### Deviation Threshold
To change the deviation threshold from 30%, edit [src/variance_engine.py](src/variance_engine.py):

```python
DEVIATION_THRESHOLD = 30  # Change this value
```

---

## 🔌 API & Extensibility

### Current Capabilities
- ✅ **CSV Import/Export** - Interchange data with Excel, Google Sheets, Power BI
- ✅ **SQLite Backend** - Query database directly for advanced analytics
- ✅ **Modular Code** - Easily extend variance_engine for custom calculations

### Connecting to External Tools

#### **Power BI Integration**
```python
# Export data from ProjectTracker
1. Use Dashboard → Download Excel
2. Open Power BI → New data source
3. Connect to exported CSV/Excel
4. Create custom visualizations
```

#### **Excel Live Connection**
```bash
# Option 1: Export routine
Run daily export → Save to shared folder
Excel pulls from folder → Auto-refresh charts

# Option 2: Direct SQLite
Excel → Data → New Query → From File → Select projecttracker.db
Create pivot tables and dashboards from live database
```

#### **Custom API Extension**
```python
# Add to src/ for REST API capabilities
from fastapi import FastAPI
from src.database import Database

app = FastAPI()
db = Database()

@app.get("/api/projects")
def get_projects():
    return db.get_all_projects()

@app.get("/api/variance/{project_id}")
def get_variance(project_id: int):
    return db.get_variance_report(project_id)

# Run: uvicorn main:app --reload
```

### Future Extensibility
- 🔮 **Webhook Support** - Trigger alerts to Slack/Teams when deviations flagged
- 🔮 **Machine Learning** - Predict future deviations based on historical trends
- 🔮 **Real-time Sync** - Connect to project management tools (Asana, Monday.com)
- 🔮 **Database Options** - Migrate from SQLite to PostgreSQL for scalability

---

## 📈 Charts & Visualizations

1. **Projected vs Actual Bar Chart** - Side-by-side comparison
2. **Deviation Chart** - Percentage deviation with 30% threshold line
3. **Sortable Analysis Table** - Filter by parameter type and status

---

## ⚠️ Error Handling & Data Validation

### Missing or Invalid Data

#### Scenario 1: Actual Value Not Provided
```
Parameter: Budget
Projected: 100
Actual: [EMPTY]

✓ Status: PENDING
✓ Variance: Not calculated
✓ Flag: None (waiting for actual value)
```

#### Scenario 2: Non-Numeric Input
```
Parameter: Timeline
Projected: 12 months
Actual: "halfway done"

❌ Error: Invalid input
✓ Response: "Please enter numeric values only"
✓ Action: Field highlighted, value rejected until corrected
```

#### Scenario 3: Negative or Zero Projected Value
```
Parameter: Cost
Projected: 0
Actual: 500

❌ Error: Division by zero in % calculation
✓ Response: "Projected value must be greater than 0"
✓ Variance: Shows as N/A (cannot calculate percentage)
```

#### Scenario 4: Missing CSV Headers
```
Uploaded CSV missing 'Parameter' or 'Projected' column

❌ Error: CSV validation failed
✓ Response: "Required columns: Parameter, Projected, Actual (optional), Unit (optional)"
✓ Example template: Auto-download and show correct format
```

### Data Validation Rules

| Rule | Input | Result |
|------|-------|--------|
| Empty Actual | Projected: 100, Actual: blank | Status: PENDING, No variance |
| Non-numeric | Projected: "a lot", Actual: 50 | ❌ Error, Field rejected |
| Zero/Negative Projected | Projected: -50, Actual: 100 | ❌ Error, Flag in red |
| Missing Parameter Name | Projected: 100, Name: blank | ❌ Error, Field required |
| Duplicate Parameter | Same name, same project | ⚠️ Warning, Allowed (versioning) |
| Invalid Date | Start date: "32/13/2026" | ❌ Error, Use date picker |

### Recovery Strategies

**If database corruption occurs:**
```bash
# 1. Backup current database
cp data/projecttracker.db data/projecttracker.db.backup

# 2. Reset database
rm data/projecttracker.db

# 3. Restart app (auto-reinitializes)
streamlit run app.py

# 4. Re-import CSV data from exports folder
```

**If CSV import fails:**
1. Download sample template from app
2. Validate headers match exactly: `Parameter,Projected,Actual,Unit`
3. Remove special characters from values
4. Ensure numbers use . (dot) not , (comma) for decimals
5. Test with sample_project.csv first

---

## 🐛 Troubleshooting

### App won't start
```bash
# Clear Streamlit cache
streamlit cache clear

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Database issues
- Delete `data/projecttracker.db` to reset (recreates on next run)
- Check file permissions in `data/` folder

### CSV import errors
- Ensure CSV has `Parameter` and `Projected` columns
- Use comma as delimiter
- Check for special characters in numeric values

---

## 📝 CSV Import Template

Save as `.csv` and import:

```
Parameter,Projected,Actual,Unit
Project Name 1,100,120,₹
Project Name 2,50,45,units
Project Name 3,12,14,months
```

---

## 🛠️ Development

### Running in development mode
```bash
streamlit run app.py --logger.level=debug
```

### File modifications auto-reload
Streamlit automatically refreshes when you modify `.py` files.

---

## 📞 Support

For issues or feature requests:
1. Check the troubleshooting section
2. Review [variance_engine.py](src/variance_engine.py) for calculation logic
3. Check database logs in `data/projecttracker.db`

---

## 📄 License

ProjectTracker © 2026. All rights reserved.

---

**Happy Tracking! 🚀**
