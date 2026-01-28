from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from enum import Enum


class IssueType(str, Enum):
    MISSING_VALUES = "missing_values"
    OUTLIERS = "outliers"
    INCONSISTENCY = "inconsistency"
    DUPLICATES = "duplicates"
    RARE_CATEGORIES = "rare_categories"


class Issue(BaseModel):
    column: str
    issue_type: IssueType
    affected_count: int
    affected_percentage: float
    severity: str  # "low", "medium", "high"
    suggested_fix: str
    recommended_operation: Dict[str, Any]


class QualityScore(BaseModel):
    completeness: float  # 0-100
    uniqueness: float    # 0-100
    consistency: float   # 0-100
    accuracy: float      # 0-100
    overall: float       # 0-100


class DatasetInfo(BaseModel):
    filename: str
    size_kb: float
    rows: int
    columns: int
    column_names: List[str]
    dtypes: Dict[str, str]
    quality_score: QualityScore


class AnalysisResult(BaseModel):
    dataset_info: DatasetInfo
    issues: List[Issue]
    preview_data: List[Dict[str, Any]]
    session_id: str


class CleaningOperation(BaseModel):
    column: str
    operation_type: str
    parameters: Dict[str, Any]
    applied_by: str  # "auto" or "user"
    rows_affected: int
    description: str


class CleaningConfig(BaseModel):
    session_id: str
    auto_clean: bool
    operations: List[CleaningOperation]


class CleaningResult(BaseModel):
    session_id: str
    cleaned_data: List[Dict[str, Any]]
    quality_before: QualityScore
    quality_after: QualityScore
    operations_applied: List[CleaningOperation]
    processing_time_ms: float
    issues_resolved: int
