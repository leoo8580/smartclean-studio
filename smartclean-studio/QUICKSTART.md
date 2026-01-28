# Quick Start Guide

## Get Running in 5 Minutes

### 1. Backend Setup (Terminal 1)

```bash
cd "c:\Users\HP\Desktop\mini 6\smartclean-studio\backend"

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start FastAPI server
uvicorn app.main:app --reload
```

Server running at: **http://localhost:8000**
API docs at: **http://localhost:8000/docs**

### 2. Frontend Setup (Terminal 2)

```bash
cd "c:\Users\HP\Desktop\mini 6\smartclean-studio\frontend"

# Install dependencies
npm install

# Start React app
npm start
```

App opens at: **http://localhost:3000**

## 3. Test the Application

1. Go to http://localhost:3000
2. Click "Start Cleaning"
3. Drag & drop a CSV/Excel file or use the browse button
4. Click "Auto Clean Now"
5. Review results and download cleaned data

## Sample Test Data

Create a test file `test_data.csv`:

```csv
ID,Name,Age,Salary,Department
1,John Doe,28,45000,Sales
2,Jane Smith,,52000,Engineering
3,Bob Johnson,35,48000,Sales
4,Alice Brown,29,65000,Engineering
5,Charlie Lee,31,,HR
6,David Wilson,45,72000,Finance
7,Emma Davis,,,Finance
8,Frank Miller,38,55000,Sales
9,Grace Lee,28,58000,Engineering
10,Henry Brown,50,75000,Management
```

This file has:
- Missing values (blank cells)
- Various numeric and text data
- Realistic data quality issues

## Stop Services

**Backend**: Press `Ctrl+C` in Terminal 1
**Frontend**: Press `Ctrl+C` in Terminal 2

## Troubleshooting

### Port Already in Use
- Backend: Change port `uvicorn app.main:app --reload --port 8001`
- Frontend: Set `PORT=3001` before `npm start`

### Module Not Found (Python)
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again

### npm Dependency Issues
- Delete `node_modules` folder and `package-lock.json`
- Run `npm install` again

### CORS Errors
- Ensure backend is running on port 8000
- Frontend automatically configured to connect to `http://localhost:8000`

## Architecture Overview

```
User Browser
     ↓
React App (3000)
     ↓ (HTTP Requests)
FastAPI Backend (8000)
     ↓
Data Analysis Engine
     ↓
Pandas/NumPy Processing
     ↓
Cleaned Dataset
```

## Key Features to Try

1. **Automatic Cleaning**: Upload file → Auto Clean → Download
2. **Issue Detection**: See detected data quality issues
3. **Quality Scores**: Before/after quality comparison
4. **Detailed Report**: See every operation applied
5. **Data Preview**: Review cleaned data before download

## Next Steps

- Modify cleaning rules in `backend/app/services/rule_engine.py`
- Customize UI in `frontend/src/pages/Dashboard.jsx`
- Add new issue detection in `backend/app/services/analyzer.py`
- Deploy to cloud (AWS, Azure, GCP)

Enjoy! 🎉
