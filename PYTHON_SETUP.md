# 🐍 Python Installation Guide for ProjectTracker

## IMPORTANT: Python is Required

Python 3.8+ is required to run ProjectTracker. Follow these steps:

---

## ✅ Windows Installation Steps

### Step 1: Download Python
1. Go to https://www.python.org/downloads/
2. Click **Download Python 3.11** (or latest 3.8+)
3. Download the `.exe` installer

### Step 2: Install Python (CRITICAL: Enable PATH)
1. Run the downloaded `.exe` file
2. **IMPORTANT:** Check the box: ✅ **"Add Python 3.x to PATH"** (bottom of window)
3. Click **"Install Now"**
4. Wait for installation to complete
5. Click **"Close"**

### Step 3: Verify Installation
Open a NEW PowerShell terminal and run:
```powershell
python --version
pip --version
```

You should see output like:
```
Python 3.11.x
pip 23.x
```

---

## Step 4: Install ProjectTracker Dependencies

Once Python is installed, run in this terminal:

```powershell
cd "c:\Users\Rahul\Project Tracker"
python -m pip install -r requirements.txt
```

Wait for all packages to install (~2-3 minutes).

---

## Step 5: Launch ProjectTracker

Run:
```powershell
streamlit run app.py
```

The dashboard will open automatically at: **http://localhost:8501**

---

## 🚀 You're Ready!

Once the Streamlit app opens:
1. Create a new project in the sidebar
2. Add parameters (or import sample_project.csv)
3. View variance analysis in the Dashboard tab

---

## ❌ Troubleshooting

**"python: The term 'python' is not recognized"**
- Python not added to PATH
- Reinstall and CHECK ✅ "Add Python to PATH"
- Restart terminal after installation

**"pip command not found"**
- Try: `python -m pip install -r requirements.txt`

**"ModuleNotFoundError"**
- Run: `python -m pip install -r requirements.txt` again

---

## 📞 Need Help?

1. Close and restart PowerShell (completely new window)
2. Verify Python: `python --version`
3. Try installation commands again

**Let me know once Python is installed and the app is running!** ✨
