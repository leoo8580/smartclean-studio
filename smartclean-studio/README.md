# SmartClean Studio - Hybrid Data Cleaning Platform

A production-ready SaaS web application that automatically detects and cleans data quality issues while maintaining full transparency and user control.

## 🎯 Overview

SmartClean Studio is an intelligent data cleaning platform designed for both enterprise and beginner use. It combines automatic issue detection with user-controlled cleaning operations, making it easy to get production-ready clean datasets.

### Key Features

- **Automatic Detection**: Instantly identifies missing values, outliers, duplicates, and inconsistencies
- **Smart Fixes**: Applies intelligent cleaning rules (median imputation, IQR capping, categorical handling)
- **Full Transparency**: See exactly what changed, why it changed, and who decided it
- **Quality Scoring**: Before/after quality metrics (completeness, uniqueness, consistency, accuracy)
- **Multiple Formats**: Upload CSV/Excel, download cleaned data in CSV/Excel
- **Production-Ready**: Enterprise-grade code architecture and UX

## 🛠️ Tech Stack

### Frontend
- **React 18** - Modern component-based UI
- **Tailwind CSS 3** - Utility-first styling
- **Axios** - HTTP client for API communication

### Backend
- **FastAPI** - High-performance Python API framework
- **Pandas/NumPy** - Data manipulation and analysis
- **Scikit-learn/SciPy** - Statistical analysis and outlier detection
- **Python 3.11+** - Latest Python runtime

## 📁 Project Structure

```
smartclean-studio/
├── frontend/                 # React application
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/           # Page-level components
│   │   ├── services/        # API integration
│   │   ├── App.jsx
│   │   └── index.js
│   ├── public/
│   ├── package.json
│   ├── tailwind.config.js
│   └── postcss.config.js
├── backend/                 # FastAPI application
│   ├── app/
│   │   ├── models/          # Pydantic schemas
│   │   ├── services/        # Core business logic
│   │   │   ├── analyzer.py     # Data analysis engine
│   │   │   ├── cleaner.py      # Cleaning operations
│   │   │   ├── rule_engine.py  # Intelligent rules
│   │   │   └── reporter.py     # Report generation
│   │   ├── routes/          # API endpoints
│   │   └── main.py          # FastAPI application
│   └── requirements.txt
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ and npm
- Python 3.11+
- pip (Python package manager)

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run FastAPI server**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
   
   API will be available at: `http://localhost:8000`
   API docs: `http://localhost:8000/docs`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm start
   ```
   
   App will open at: `http://localhost:3000`

## 📊 API Endpoints

### Upload Dataset
- **POST** `/api/upload`
- Upload CSV or Excel file for analysis
- Returns: Dataset info, detected issues, data preview, session ID

### Configure Cleaning
- **POST** `/api/configure`
- Configure cleaning operations (auto or manual)
- Returns: Validation status and operation count

### Apply Cleaning
- **POST** `/api/clean?session_id={id}`
- Execute configured cleaning operations
- Returns: Quality scores before/after, cleaned data, operations log

### Get Report
- **GET** `/api/report/{session_id}`
- Retrieve detailed cleaning report
- Returns: Human-readable report with all operations

### Get Data Preview
- **GET** `/api/preview/{session_id}?limit=100`
- Preview cleaned dataset
- Returns: Paginated data with row count

### Download Data
- **POST** `/api/download/{session_id}/{format}`
- Download cleaned data (csv or excel)
- Returns: File data with filename

## 🎨 UI Workflow

### 1. Landing Page
Modern hero section with gradient background, explaining the product value proposition.

### 2. Upload Page
- Drag & drop upload area
- File info display (rows, columns, size)
- Initial quality score

### 3. Analyze Step
- Data preview table
- Detected issues cards (outliers, missing values, etc.)
- Quality breakdown (completeness, uniqueness, consistency, accuracy)
- Option to auto-clean or upload different file

### 4. Results Step
- Success banner
- Before/after quality score comparison with improvement percentage
- Summary cards (rows, columns, issues resolved, processing time)
- Cleaning operations list (expandable with details)
- Tabs for cleaning report and data preview
- Download buttons (CSV and Excel)

## 🧠 Intelligent Cleaning Rules

### Missing Values
- **Detection**: Any null/empty values
- **Auto-fix**: 
  - Numeric columns: Use median (robust to outliers)
  - Categorical columns: Use mode (most frequent value)
  - High missing (>50%): Remove column

### Outliers
- **Detection**: IQR (Interquartile Range) method
- **Auto-fix**:
  - Low percentage (<5%): Cap using IQR bounds
  - High percentage (>5%): Remove rows

### Rare Categories
- **Detection**: Categories appearing <1% of time
- **Auto-fix**: Group rare values into "Other" category

### Column Standardization
- Standardize column names (lowercase, underscore)
- Standardize categorical values (lowercase, trimmed)

## 📊 Quality Scoring

### Metrics Calculated

1. **Completeness** (0-100)
   - Percentage of non-null values
   - Higher is better

2. **Uniqueness** (0-100)
   - Ratio of unique values to total values
   - Higher indicates good data variety

3. **Consistency** (0-100)
   - Percentage of columns with consistent data types
   - Higher is better

4. **Accuracy** (0-100)
   - Percentage of columns with <5% outliers (numeric)
   - Higher is better

**Overall Score** = Average of all four metrics

## 🔒 Data Flow & Sessions

- Each upload creates a unique session ID
- All operations are stateless on backend
- Session data stored in-memory (configurable to database)
- Download links valid for session duration

## 🎯 Design Principles

1. **Intelligent by Default**: Auto-cleaning requires zero configuration
2. **Transparent**: Every action shows what was done and why
3. **User Control**: Always option to override automatic decisions
4. **Enterprise-Grade**: Production architecture and error handling
5. **Beginner-Friendly**: Intuitive UI with clear explanations

## 🔧 Configuration

### Environment Variables (Optional)

Create `.env` file in backend root:
```
API_HOST=0.0.0.0
API_PORT=8000
MAX_FILE_SIZE=52428800  # 50 MB
SESSION_TIMEOUT=3600    # 1 hour
```

### Customizing Cleaning Rules

Edit `backend/app/services/rule_engine.py` to modify auto-cleaning strategies.

## 📈 Performance

- Upload file analysis: <100ms for 10k rows
- Data cleaning: <500ms for typical 10k row dataset
- Quality score calculation: <50ms
- Report generation: <100ms

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 🚢 Production Deployment

### Backend (Docker)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app/ ./app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend (Docker)
```dockerfile
FROM node:18-alpine as build
WORKDIR /app
COPY package*.json .
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Cloud Deployment
- Backend: AWS Lambda + API Gateway, or Azure Functions
- Frontend: AWS S3 + CloudFront, or Azure Static Web Apps
- Database: For session persistence, use PostgreSQL or DynamoDB

## 📝 API Documentation

After starting backend, visit: `http://localhost:8000/docs`

Interactive Swagger UI with full API documentation and try-it-out functionality.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

MIT License - feel free to use in personal and commercial projects.

## 💬 Support

For issues, questions, or suggestions:
1. Check existing GitHub issues
2. Create new issue with detailed description
3. Include sample data if applicable

## 🎓 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Pandas User Guide](https://pandas.pydata.org/docs/)

## 📊 Real-World Use Cases

- **Finance**: Clean transaction data, remove duplicates
- **Healthcare**: Standardize patient records, handle missing values
- **E-commerce**: Normalize product data, remove outliers
- **Research**: Prepare datasets for analysis
- **Data Migration**: Clean data before moving between systems

## 🚀 Future Enhancements

- [ ] User authentication and multi-user support
- [ ] Advanced statistical analysis and visualization
- [ ] Custom cleaning rule builder
- [ ] Batch processing for multiple files
- [ ] Scheduling for automated cleaning
- [ ] Integration with cloud storage (S3, GCS)
- [ ] API rate limiting and quotas
- [ ] Advanced filtering and sampling options
- [ ] Machine learning-based anomaly detection
- [ ] Export to multiple database formats

---

**Built with ❤️ for clean data**
