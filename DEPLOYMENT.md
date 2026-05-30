# 🚀 Deployment Guide - ProjectTracker

## Streamlit Cloud Deployment

### Quick Start (2 minutes)

1. **Go to Streamlit Cloud**
   ```
   https://share.streamlit.io/
   ```

2. **Sign In with GitHub**
   - Click "Sign in with GitHub"
   - Authorize Streamlit to access your repositories
   - Verify your email

3. **Deploy the App**
   - Click "New app" button
   - Repository: `rahulsti07/Real-Estate-Project-Tracker`
   - Branch: `main`
   - Main file path: `app.py`
   - Click "Deploy"

4. **Wait for Build**
   - Build takes 2-3 minutes
   - Watch the logs
   - Your app will be live at:
     ```
     https://<your-username>-real-estate-project-tracker.streamlit.app
     ```

---

## ✅ What's Pre-configured

✓ `requirements.txt` - All dependencies listed
✓ `.streamlit/config.toml` - Optimal settings
✓ `.streamlit/secrets.toml.example` - Template for secrets
✓ `data/projecttracker.db` - SQLite database

---

## 🔐 Setting Up Secrets (Optional)

If you add API keys or sensitive data:

1. Go to your app in Streamlit Cloud
2. Click **⋮ (menu) → Settings**
3. Go to **Secrets** tab
4. Copy content from `.streamlit/secrets.toml.example`
5. Add your actual values
6. Click "Save"

---

## 📊 Database Notes

- **Local:** Uses `data/projecttracker.db` (SQLite)
- **Cloud:** Same SQLite file is deployed with the app
- **Data Persistence:** Data persists across restarts
- **Backup:** Download database from GitHub repo

---

## 🛠️ Troubleshooting

### App won't start
- Check `requirements.txt` is in root directory
- Check `app.py` is in root directory
- Check Python version compatibility (3.8+)

### Database errors
- Ensure `data/` folder exists
- Database auto-creates on first run
- Check file permissions

### Import errors
- Run `pip install -r requirements.txt` locally first
- Verify all imports in `app.py` match `requirements.txt`

---

## 📱 Sharing Your App

Once deployed, share the URL:
```
https://<your-username>-real-estate-project-tracker.streamlit.app
```

Anyone can access it (no GitHub login required)

---

## 🔄 Auto-Deployment

Any push to `main` branch automatically triggers redeployment:
```bash
git push origin main
```

Your app will redeploy with latest changes in ~2 minutes.

---

## 📚 More Resources

- Streamlit Docs: https://docs.streamlit.io/
- Deployment Guide: https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app
- Secrets Management: https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management
