# Architecture Overview

## System Design

SmartClean Studio follows a clean, modular architecture with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                    User Browser                            │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────────┐
│            React Frontend (Port 3000)                        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Pages: Landing, Dashboard, Upload, Results        │   │
│  │  Components: Stepper, QualityScore, IssueCard       │   │
│  │  Services: API client with Axios                    │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP REST
                     ↓
┌─────────────────────────────────────────────────────────────┐
│            FastAPI Backend (Port 8000)                       │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Routes:                                            │   │
│  │  - POST /api/upload      (File processing)         │   │
│  │  - POST /api/configure   (Config validation)        │   │
│  │  - POST /api/clean       (Apply operations)         │   │
│  │  - GET /api/report       (Report generation)        │   │
│  │  - GET /api/preview      (Data preview)             │   │
│  │  - POST /api/download    (Export cleaned data)      │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Services:                                          │   │
│  │  ┌────────────────────────────────────────────────┐ │   │
│  │  │ Analyzer                                       │ │   │
│  │  │ - Data profiling                              │ │   │
│  │  │ - Issue detection                             │ │   │
│  │  │ - Quality scoring                             │ │   │
│  │  └────────────────────────────────────────────────┘ │   │
│  │  ┌────────────────────────────────────────────────┐ │   │
│  │  │ RuleEngine                                     │ │   │
│  │  │ - Auto-plan generation                        │ │   │
│  │  │ - Operation validation                        │ │   │
│  │  │ - Safety checks                               │ │   │
│  │  └────────────────────────────────────────────────┘ │   │
│  │  ┌────────────────────────────────────────────────┐ │   │
│  │  │ Cleaner                                        │ │   │
│  │  │ - Apply operations                            │ │   │
│  │  │ - Imputation                                  │ │   │
│  │  │ - Outlier handling                            │ │   │
│  │  │ - Standardization                             │ │   │
│  │  └────────────────────────────────────────────────┘ │   │
│  │  ┌────────────────────────────────────────────────┐ │   │
│  │  │ Reporter                                       │ │   │
│  │  │ - Report generation                           │ │   │
│  │  │ - Human-readable descriptions                 │ │   │
│  │  └────────────────────────────────────────────────┘ │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Models (Pydantic Schemas):                         │   │
│  │  - Request/Response validation                     │   │
│  │  - Type safety                                     │   │
│  │  - Auto documentation                             │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ↓
        ┌────────────────────────┐
        │  Data Processing      │
        ├────────────────────────┤
        │  Pandas/NumPy          │
        │  Scikit-learn          │
        │  SciPy                 │
        └────────────────────────┘
```

## Data Flow

### 1. Upload Phase
```
CSV/Excel File
    ↓
[Frontend Upload]
    ↓
[POST /api/upload]
    ↓
[Analyzer.analyze()]
    ├─ _get_dataset_info()      → Metadata
    ├─ _calculate_quality_score() → Before score
    └─ _detect_issues()          → Issue list
    ↓
[Session Creation]
    └─ Store df, analysis, metadata
    ↓
[Return to Frontend]
    └─ Analysis result + session ID
```

### 2. Cleaning Phase
```
[Configure Request]
    ↓
[POST /api/configure]
    ├─ If auto_clean: RuleEngine.generate_auto_cleaning_plan()
    └─ Validate all operations
    ↓
[POST /api/clean]
    ↓
[Cleaner.apply_operations()]
    ├─ _impute_missing()
    ├─ _handle_outliers()
    ├─ _group_rare_categories()
    ├─ _standardize_column()
    └─ _normalize_values()
    ↓
[Calculate Quality After]
    ├─ Analyzer.analyze()
    └─ Compare before/after
    ↓
[Reporter.generate_report()]
    ├─ Summary statistics
    ├─ Quality improvements
    └─ Operation details
    ↓
[Return CleaningResult]
    └─ Cleaned data + metrics + operations log
```

### 3. Download Phase
```
[User requests download]
    ↓
[POST /api/download/{session_id}/{format}]
    ├─ If format == 'csv': Pandas to_csv()
    └─ If format == 'excel': Pandas to_excel()
    ↓
[Return file data]
    ↓
[Frontend downloads file]
```

## Component Relationships

```
┌─────────────────────────────────────────┐
│         Frontend Components             │
├─────────────────────────────────────────┤
│ App.jsx                                 │
│ ├─ LandingPage                          │
│ └─ Dashboard                            │
│    ├─ UploadBox                         │
│    ├─ Stepper                           │
│    ├─ IssueCard (x many)                │
│    ├─ QualityScore (x 2)                │
│    ├─ DataTable                         │
│    └─ Button (x many)                   │
└─────────────────────────────────────────┘
         ↓ (API calls)
┌─────────────────────────────────────────┐
│    Backend Services (Modular)           │
├─────────────────────────────────────────┤
│ RuleEngine                              │
│ ├─ generate_auto_cleaning_plan()        │
│ └─ validate_operation()                 │
│                                         │
│ Analyzer                                │
│ ├─ analyze()                            │
│ ├─ _detect_issues()                     │
│ └─ _calculate_quality_score()           │
│                                         │
│ Cleaner                                 │
│ ├─ apply_operations()                   │
│ ├─ _impute_missing()                    │
│ ├─ _handle_outliers()                   │
│ └─ get_cleaned_data()                   │
│                                         │
│ Reporter                                │
│ ├─ generate_report()                    │
│ └─ get_human_readable_report()          │
└─────────────────────────────────────────┘
```

## Session Management

Sessions are stored in-memory with the following structure:

```python
sessions[session_id] = {
    'df': DataFrame,                   # Original dataset
    'filename': str,                   # Original filename
    'dataset_info': DatasetInfo,       # Metadata
    'issues': List[Issue],             # Detected issues
    'preview': List[Dict],             # Data preview
    'quality_before': QualityScore,    # Initial quality
    'cleaning_config': CleaningConfig, # User config
    'cleaned_df': DataFrame,           # Cleaned version
    'quality_after': QualityScore,     # Final quality
    'operations_applied': List[...],   # Applied ops
    'report': Dict                     # Generated report
}
```

## Quality Scoring Algorithm

```
Completeness = (non_null_cells / total_cells) × 100

Uniqueness = (unique_values / total_cells) × 100

Consistency = (consistent_columns / total_columns) × 100

Accuracy = (columns_with_<5%_outliers / numeric_columns) × 100

Overall = (Completeness + Uniqueness + Consistency + Accuracy) / 4
```

## Error Handling

```
User Input
    ↓
[Validation]
    ├─ File type check
    ├─ File size check
    └─ Data format validation
    ↓
[If invalid] → HTTPException (400)
    ↓
[If valid]
    ↓
[Processing]
    ├─ Try-Except wrapping
    └─ Detailed error logging
    ↓
[If error] → HTTPException (400-500)
    ↓
[If success] → JSON Response
```

## Scalability Considerations

### Current (Development)
- In-memory session storage
- Single process
- File-based operations
- Suitable for: Testing, demos, small datasets

### Production Ready (Recommendations)
- **Session Storage**: Redis/DynamoDB for distributed sessions
- **File Storage**: S3/GCS for uploaded and processed files
- **Queue System**: Celery/RQ for async processing
- **Monitoring**: Prometheus + Grafana for metrics
- **Logging**: Structured logging with ELK stack
- **Load Balancing**: Nginx/HAProxy for API
- **Caching**: Redis for frequently accessed data

### Deployment Patterns
```
Load Balancer
    ↓
API Gateway (FastAPI)
    ├─ Instance 1
    ├─ Instance 2
    └─ Instance N
    ↓
Shared Resources
├─ Redis (Sessions)
├─ PostgreSQL (Logs)
├─ S3 (Files)
└─ Message Queue (Jobs)
```

## Security Considerations

1. **Input Validation**: All API inputs validated with Pydantic
2. **File Upload**: Size limits and type checking
3. **CORS**: Configurable cross-origin requests
4. **Error Handling**: No sensitive data in error messages
5. **Session**: Should implement user authentication
6. **Rate Limiting**: Can be added with slowapi/fastapi-limiter

---

This architecture ensures:
- ✓ Clear separation of concerns
- ✓ Testability at each layer
- ✓ Scalability and maintainability
- ✓ Easy to extend and modify
- ✓ Production-grade structure
