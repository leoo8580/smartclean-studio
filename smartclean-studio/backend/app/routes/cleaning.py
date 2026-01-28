from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
import pandas as pd
import io
import time
import tempfile
import os
from uuid import uuid4
from models.schemas import (
    AnalysisResult, CleaningConfig, CleaningResult, CleaningOperation
)
from services.analyzer import DataAnalyzer, convert_to_native_types
from services.cleaner import DataCleaner
from services.rule_engine import RuleEngine
from services.reporter import Reporter

router = APIRouter()

# Session storage (in-memory for now)
sessions = {}


@router.post("/upload")
async def upload_dataset(file: UploadFile = File(...)):
    """Upload and analyze dataset"""
    try:
        # Read file
        contents = await file.read()
        
        # Determine file type
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents), dtype=str)  # Read all as strings first
        elif file.filename.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(io.BytesIO(contents))
        else:
            raise HTTPException(status_code=400, detail="File must be CSV or Excel")

        # Convert all columns to native Python types immediately
        for col in df.columns:
            # Try to convert numeric columns
            try:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            except:
                # Keep as string if conversion fails
                df[col] = df[col].astype(str)

        # Calculate file size
        size_kb = len(contents) / 1024

        # Analyze dataset
        analyzer = DataAnalyzer(df, file.filename, size_kb)
        dataset_info, issues, preview = analyzer.analyze()

        # Create session
        session_id = str(uuid4())
        sessions[session_id] = {
            'df': df,
            'filename': file.filename,
            'dataset_info': dataset_info,
            'issues': issues,
            'preview': preview,
            'quality_before': dataset_info.quality_score,
            'cleaning_config': None
        }

        return AnalysisResult(
            dataset_info=dataset_info,
            issues=issues,
            preview_data=preview,
            session_id=session_id
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/configure")
async def configure_cleaning(config: CleaningConfig):
    """Configure cleaning operations before applying"""
    session_id = config.session_id

    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = sessions[session_id]
    df = session['df']

    # If auto_clean is True, generate automatic operations
    if config.auto_clean:
        auto_operations = RuleEngine.generate_auto_cleaning_plan(df, session['issues'])
        config.operations = [
            CleaningOperation(
                column=op['column'],
                operation_type=op['operation'],
                parameters=op['parameters'],
                applied_by='auto',
                rows_affected=0,
                description=''
            )
            for op in auto_operations
        ]

    # Validate all operations
    for operation in config.operations:
        if not RuleEngine.validate_operation({
            'column': operation.column,
            'operation': operation.operation_type
        }, df):
            return {
                'status': 'error',
                'message': f'Invalid operation on column {operation.column}'
            }

    session['cleaning_config'] = config
    return {'status': 'configured', 'operations_count': len(config.operations)}


@router.post("/clean")
async def apply_cleaning(session_id: str):
    """Apply cleaning operations and return results"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = sessions[session_id]
    df = session['df']
    config = session.get('cleaning_config')

    if not config:
        raise HTTPException(status_code=400, detail="No cleaning config found. Please configure first.")

    start_time = time.time()

    # Apply cleaning
    cleaner = DataCleaner(df)
    
    operations_dicts = [
        {
            'column': op.column,
            'operation': op.operation_type,
            'parameters': op.parameters
        }
        for op in config.operations
    ]
    
    cleaned_df = cleaner.apply_operations(operations_dicts, auto_mode=config.auto_clean)
    operations_applied = cleaner.get_operations_log()

    processing_time_ms = (time.time() - start_time) * 1000

    # Calculate quality after cleaning
    analyzer_after = DataAnalyzer(cleaned_df, session['filename'], 0)
    quality_after = analyzer_after._calculate_quality_score()

    # Prepare cleaned data for JSON serialization
    cleaned_data_preview = cleaned_df.head(100).copy()
    cleaned_data_preview = convert_to_native_types(cleaned_data_preview)
    
    # Prepare report data
    report_data_preview = cleaned_df.head(10).copy()
    report_data_preview = convert_to_native_types(report_data_preview)

    # Generate report
    report = Reporter.generate_report(
        report_data_preview.to_dict(orient='records'),
        operations_applied,
        session['quality_before'],
        quality_after,
        processing_time_ms
    )

    # Store result
    session['cleaned_df'] = cleaned_df
    session['quality_after'] = quality_after
    session['operations_applied'] = operations_applied
    session['report'] = report

    return CleaningResult(
        session_id=session_id,
        cleaned_data=cleaned_data_preview.to_dict(orient='records'),
        quality_before=session['quality_before'],
        quality_after=quality_after,
        operations_applied=operations_applied,
        processing_time_ms=processing_time_ms,
        issues_resolved=len(operations_applied)
    )


@router.get("/report/{session_id}")
async def get_report(session_id: str):
    """Get detailed cleaning report"""
    if session_id not in sessions or 'report' not in sessions[session_id]:
        raise HTTPException(status_code=404, detail="Report not found")

    return sessions[session_id]['report']


@router.get("/preview/{session_id}")
async def get_data_preview(session_id: str, limit: int = 100):
    """Get preview of cleaned data"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = sessions[session_id]
    if 'cleaned_df' not in session:
        raise HTTPException(status_code=400, detail="Data not cleaned yet")

    data = session['cleaned_df'].head(limit).to_dict(orient='records')
    return {'data': data, 'total_rows': len(session['cleaned_df'])}


@router.post("/download/{session_id}/{format}")
async def download_data(session_id: str, format: str):
    """Download cleaned data in CSV or Excel format"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = sessions[session_id]
    if 'cleaned_df' not in session:
        raise HTTPException(status_code=400, detail="Data not cleaned yet")

    # Get the cleaned dataframe - DO NOT convert to native types for export
    df = session['cleaned_df'].copy()
    
    # Only fill NaN with "N/A" string for display
    df = df.fillna("N/A")
    
    if format == 'csv':
        # Generate CSV in memory
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_content = csv_buffer.getvalue()
        
        # Create temporary file for streaming
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.csv', mode='w', encoding='utf-8')
        temp_path = temp_file.name
        temp_file.write(csv_content)
        temp_file.close()
        
        try:
            return FileResponse(
                path=temp_path,
                media_type="text/csv",
                filename="cleaned_data.csv"
            )
        except Exception as e:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise HTTPException(status_code=500, detail=f"CSV export failed: {str(e)}")
    
    elif format == 'excel' or format == 'xlsx':
        try:
            # Generate Excel in memory
            excel_buffer = io.BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='Cleaned Data', index=False)
            
            excel_buffer.seek(0)
            excel_bytes = excel_buffer.getvalue()
            
            # Create temporary file for streaming
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx', mode='wb')
            temp_path = temp_file.name
            temp_file.write(excel_bytes)
            temp_file.close()
            
            return FileResponse(
                path=temp_path,
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                filename="cleaned_data.xlsx"
            )
        except Exception as e:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise HTTPException(status_code=500, detail=f"Excel export failed: {str(e)}")
    
    else:
        raise HTTPException(status_code=400, detail="Invalid format. Use 'csv' or 'excel'")
