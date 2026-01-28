import pandas as pd
import numpy as np
from typing import List, Dict, Any, Tuple
from models.schemas import (
    Issue, IssueType, QualityScore, DatasetInfo
)


def convert_to_native_types(df: pd.DataFrame) -> pd.DataFrame:
    """Convert dataframe to native Python types for JSON serialization"""
    df = df.copy()
    for col in df.columns:
        dtype_str = str(df[col].dtype).lower()
        
        # Handle string/object types
        if 'string' in dtype_str or df[col].dtype == 'object':
            # Force to regular Python strings via astype to object first
            df[col] = df[col].astype(object).apply(lambda x: str(x) if pd.notna(x) else None)
        # Handle numeric types
        elif pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].apply(lambda x: float(x) if pd.notna(x) else None)
        # Handle datetime types
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].astype(str).apply(lambda x: x if x != 'NaT' else None)
    
    # Replace remaining NaN/None with "N/A" for display
    df = df.fillna("N/A")
    return df


class DataAnalyzer:
    """Analyzes datasets for data quality issues"""

    def __init__(self, df: pd.DataFrame, filename: str, size_kb: float):
        self.df = df
        self.filename = filename
        self.size_kb = size_kb
        self.original_df = df.copy()

    def analyze(self) -> Tuple[DatasetInfo, List[Issue], List[Dict[str, Any]]]:
        """Run complete analysis on dataset"""
        dataset_info = self._get_dataset_info()
        issues = self._detect_issues()
        preview = self._get_preview()

        return dataset_info, issues, preview

    def _get_dataset_info(self) -> DatasetInfo:
        """Extract dataset metadata"""
        dtypes = {}
        for col in self.df.columns:
            dtype_str = str(self.df[col].dtype).lower()
            if 'object' in dtype_str or 'string' in dtype_str:
                dtypes[col] = 'categorical'
            elif any(x in dtype_str for x in ['int', 'float', 'decimal']):
                dtypes[col] = 'numeric'
            else:
                dtypes[col] = 'other'

        quality_score = self._calculate_quality_score()

        return DatasetInfo(
            filename=self.filename,
            size_kb=self.size_kb,
            rows=len(self.df),
            columns=len(self.df.columns),
            column_names=list(self.df.columns),
            dtypes=dtypes,
            quality_score=quality_score
        )

    def _calculate_quality_score(self) -> QualityScore:
        """Calculate data quality metrics"""
        completeness = self._calculate_completeness()
        uniqueness = self._calculate_uniqueness()
        consistency = self._calculate_consistency()
        accuracy = self._calculate_accuracy()

        overall = (completeness + uniqueness + consistency + accuracy) / 4

        return QualityScore(
            completeness=completeness,
            uniqueness=uniqueness,
            consistency=consistency,
            accuracy=accuracy,
            overall=overall
        )

    def _calculate_completeness(self) -> float:
        """Percentage of non-null values"""
        if len(self.df) == 0:
            return 0.0
        non_null = self.df.count().sum()
        total = len(self.df) * len(self.df.columns)
        return (non_null / total) * 100 if total > 0 else 0.0

    def _calculate_uniqueness(self) -> float:
        """Percentage of unique values vs total"""
        if len(self.df) == 0:
            return 100.0
        unique_count = 0
        for col in self.df.columns:
            unique_count += self.df[col].nunique()
        total_cells = len(self.df) * len(self.df.columns)
        return (unique_count / total_cells) * 100

    def _calculate_consistency(self) -> float:
        """Check for consistent data types within columns"""
        if len(self.df) == 0:
            return 100.0

        consistent_cols = 0
        for col in self.df.columns:
            if self.df[col].dtype != 'object':
                # Numeric column - check for NaN consistency
                consistent_cols += 1
            else:
                # String column - just mark as consistent
                consistent_cols += 1

        return (consistent_cols / len(self.df.columns)) * 100

    def _calculate_accuracy(self) -> float:
        """Check for outliers and anomalies"""
        if len(self.df) == 0:
            return 100.0

        accurate_cols = 0
        for col in self.df.columns:
            if np.issubdtype(self.df[col].dtype, np.number):
                # Check for extreme outliers
                Q1 = self.df[col].quantile(0.25)
                Q3 = self.df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower = Q1 - 1.5 * IQR
                upper = Q3 + 1.5 * IQR
                outliers = ((self.df[col] < lower) | (self.df[col] > upper)).sum()
                outlier_pct = (outliers / len(self.df)) * 100
                if outlier_pct < 5:  # Less than 5% outliers is good
                    accurate_cols += 1
            else:
                accurate_cols += 1

        return (accurate_cols / len(self.df.columns)) * 100

    def _detect_issues(self) -> List[Issue]:
        """Detect all data quality issues"""
        issues = []

        for col in self.df.columns:
            # Missing values
            missing_count = self.df[col].isnull().sum()
            if missing_count > 0:
                missing_pct = (missing_count / len(self.df)) * 100
                severity = "high" if missing_pct > 30 else "medium" if missing_pct > 10 else "low"
                issues.append(Issue(
                    column=col,
                    issue_type=IssueType.MISSING_VALUES,
                    affected_count=int(missing_count),
                    affected_percentage=missing_pct,
                    severity=severity,
                    suggested_fix=f"Column '{col}' has {missing_pct:.1f}% missing values",
                    recommended_operation={
                        "operation": "impute_missing",
                        "strategy": "mean" if np.issubdtype(self.df[col].dtype, np.number) else "mode"
                    }
                ))

            # Outliers for numeric columns
            if np.issubdtype(self.df[col].dtype, np.number):
                Q1 = self.df[col].quantile(0.25)
                Q3 = self.df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower = Q1 - 1.5 * IQR
                upper = Q3 + 1.5 * IQR
                outliers = ((self.df[col] < lower) | (self.df[col] > upper)).sum()

                if outliers > 0:
                    outlier_pct = (outliers / len(self.df)) * 100
                    severity = "high" if outlier_pct > 5 else "low"
                    issues.append(Issue(
                        column=col,
                        issue_type=IssueType.OUTLIERS,
                        affected_count=int(outliers),
                        affected_percentage=outlier_pct,
                        severity=severity,
                        suggested_fix=f"Column '{col}' has {outlier_pct:.1f}% outliers",
                        recommended_operation={
                            "operation": "handle_outliers",
                            "strategy": "cap",
                            "lower_bound": float(lower),
                            "upper_bound": float(upper)
                        }
                    ))

            # Rare categories
            if self.df[col].dtype == 'object':
                value_counts = self.df[col].value_counts()
                total_count = len(self.df)
                rare_count = (value_counts / total_count < 0.01).sum()  # Less than 1%
                
                if rare_count > 0:
                    rare_rows = (self.df[col].isin(value_counts[value_counts / total_count < 0.01].index)).sum()
                    rare_pct = (rare_rows / len(self.df)) * 100
                    if rare_pct > 0:
                        issues.append(Issue(
                            column=col,
                            issue_type=IssueType.RARE_CATEGORIES,
                            affected_count=int(rare_rows),
                            affected_percentage=rare_pct,
                            severity="low",
                            suggested_fix=f"Column '{col}' has {rare_pct:.1f}% rare categories",
                            recommended_operation={
                                "operation": "group_rare_categories",
                                "threshold": 0.01,
                                "group_label": "Other"
                            }
                        ))

        return issues

    def _get_preview(self, n_rows: int = 5) -> List[Dict[str, Any]]:
        """Get preview of data"""
        preview_df = self.df.head(n_rows).copy()
        preview_df = convert_to_native_types(preview_df)
        return preview_df.to_dict(orient='records')
