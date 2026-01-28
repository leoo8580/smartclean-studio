import pandas as pd
import numpy as np
from typing import List, Dict, Any
from models.schemas import CleaningOperation, QualityScore


class DataCleaner:
    """Applies cleaning operations to datasets"""

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.original_df = df.copy()
        self.operations_log: List[CleaningOperation] = []

    def apply_operations(self, operations: List[Dict[str, Any]], auto_mode: bool = True) -> pd.DataFrame:
        """Apply a series of cleaning operations"""
        for op in operations:
            self._apply_operation(op, applied_by="auto" if auto_mode else "user")
        return self.df

    def _apply_operation(self, operation: Dict[str, Any], applied_by: str = "auto"):
        """Apply single cleaning operation"""
        op_type = operation.get('operation')
        col = operation.get('column')
        params = operation.get('parameters', {})

        rows_before = len(self.df)

        if op_type == 'impute_missing':
            self._impute_missing(col, params)
        elif op_type == 'handle_outliers':
            self._handle_outliers(col, params)
        elif op_type == 'group_rare_categories':
            self._group_rare_categories(col, params)
        elif op_type == 'standardize_column':
            self._standardize_column(col, params)
        elif op_type == 'normalize_values':
            self._normalize_values(col, params)

        rows_after = len(self.df)
        rows_affected = rows_before - rows_after

        self.operations_log.append(CleaningOperation(
            column=col,
            operation_type=op_type,
            parameters=params,
            applied_by=applied_by,
            rows_affected=max(0, rows_affected),
            description=self._get_operation_description(op_type, col, params)
        ))

    def _impute_missing(self, column: str, params: Dict[str, Any]):
        """Fill missing values using specified strategy"""
        strategy = params.get('strategy', 'mean')

        if column not in self.df.columns:
            return

        if strategy == 'mean':
            if np.issubdtype(self.df[column].dtype, np.number):
                fill_value = self.df[column].mean()
                self.df[column] = self.df[column].fillna(fill_value)
        elif strategy == 'median':
            if np.issubdtype(self.df[column].dtype, np.number):
                fill_value = self.df[column].median()
                self.df[column] = self.df[column].fillna(fill_value)
        elif strategy == 'mode':
            fill_value = self.df[column].mode()[0] if not self.df[column].mode().empty else 'Unknown'
            self.df[column] = self.df[column].fillna(fill_value)
        elif strategy == 'remove':
            self.df = self.df[self.df[column].notna()].copy()

    def _handle_outliers(self, column: str, params: Dict[str, Any]):
        """Handle outliers using IQR method"""
        if column not in self.df.columns or not np.issubdtype(self.df[column].dtype, np.number):
            return

        strategy = params.get('strategy', 'cap')
        lower_bound = params.get('lower_bound')
        upper_bound = params.get('upper_bound')

        if lower_bound is None or upper_bound is None:
            Q1 = self.df[column].quantile(0.25)
            Q3 = self.df[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

        if strategy == 'cap':
            self.df[column] = self.df[column].clip(lower=lower_bound, upper=upper_bound)
        elif strategy == 'remove':
            self.df = self.df[(self.df[column] >= lower_bound) & (self.df[column] <= upper_bound)]

    def _group_rare_categories(self, column: str, params: Dict[str, Any]):
        """Replace rare categories with 'Other'"""
        if column not in self.df.columns or self.df[column].dtype != 'object':
            return

        threshold = params.get('threshold', 0.01)
        group_label = params.get('group_label', 'Other')

        value_counts = self.df[column].value_counts()
        rare_categories = value_counts[value_counts / len(self.df) < threshold].index

        self.df[column] = self.df[column].replace(rare_categories, group_label)

    def _standardize_column(self, column: str, params: Dict[str, Any]):
        """Standardize column names and values"""
        if column not in self.df.columns:
            return

        # Standardize column name
        new_name = column.lower().strip().replace(' ', '_')
        if new_name != column:
            self.df.rename(columns={column: new_name}, inplace=True)

        # Standardize values for categorical columns
        if self.df[new_name].dtype == 'object':
            self.df[new_name] = self.df[new_name].str.strip().str.lower()

    def _normalize_values(self, column: str, params: Dict[str, Any]):
        """Normalize numeric values"""
        if column not in self.df.columns or not np.issubdtype(self.df[column].dtype, np.number):
            return

        method = params.get('method', 'minmax')

        if method == 'minmax':
            min_val = self.df[column].min()
            max_val = self.df[column].max()
            if max_val != min_val:
                self.df[column] = (self.df[column] - min_val) / (max_val - min_val)
        elif method == 'zscore':
            mean = self.df[column].mean()
            std = self.df[column].std()
            if std != 0:
                self.df[column] = (self.df[column] - mean) / std

    def _get_operation_description(self, op_type: str, column: str, params: Dict[str, Any]) -> str:
        """Generate human-readable description of operation"""
        if op_type == 'impute_missing':
            strategy = params.get('strategy', 'mean')
            return f"Filled missing values in '{column}' using {strategy}"
        elif op_type == 'handle_outliers':
            strategy = params.get('strategy', 'cap')
            if strategy == 'cap':
                return f"Capped outliers in '{column}' using IQR method"
            else:
                return f"Removed outliers from '{column}'"
        elif op_type == 'group_rare_categories':
            return f"Grouped rare categories in '{column}' to 'Other'"
        elif op_type == 'standardize_column':
            return f"Standardized column name and values in '{column}'"
        elif op_type == 'normalize_values':
            method = params.get('method', 'minmax')
            return f"Normalized '{column}' using {method} scaling"
        return f"Applied {op_type} to '{column}'"

    def get_cleaned_data(self) -> pd.DataFrame:
        """Get the cleaned dataframe"""
        return self.df

    def get_operations_log(self) -> List[CleaningOperation]:
        """Get list of applied operations"""
        return self.operations_log
