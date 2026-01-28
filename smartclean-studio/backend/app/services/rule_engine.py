import pandas as pd
import numpy as np
from typing import List, Dict, Any
from models.schemas import Issue, IssueType


class RuleEngine:
    """Applies intelligent cleaning rules"""

    @staticmethod
    def generate_auto_cleaning_plan(df: pd.DataFrame, issues: List[Issue]) -> List[Dict[str, Any]]:
        """Generate automatic cleaning operations based on detected issues"""
        operations = []

        for issue in issues:
            if issue.issue_type == IssueType.MISSING_VALUES:
                operations.append(RuleEngine._handle_missing_values_rule(df, issue))
            elif issue.issue_type == IssueType.OUTLIERS:
                operations.append(RuleEngine._handle_outliers_rule(df, issue))
            elif issue.issue_type == IssueType.RARE_CATEGORIES:
                operations.append(RuleEngine._handle_rare_categories_rule(df, issue))

        # Always standardize column names
        operations.insert(0, {
            'column': 'all',
            'operation': 'standardize_column_names',
            'parameters': {}
        })

        return operations

    @staticmethod
    def _handle_missing_values_rule(df: pd.DataFrame, issue: Issue) -> Dict[str, Any]:
        """Generate operation for missing values"""
        col = issue.column
        missing_pct = issue.affected_percentage

        # Decide strategy based on percentage
        if missing_pct > 50:
            strategy = 'remove'  # Remove column with >50% missing
        elif np.issubdtype(df[col].dtype, np.number):
            strategy = 'median'  # Use median for numeric (robust to outliers)
        else:
            strategy = 'mode'  # Use mode for categorical

        return {
            'column': col,
            'operation': 'impute_missing',
            'parameters': {'strategy': strategy}
        }

    @staticmethod
    def _handle_outliers_rule(df: pd.DataFrame, issue: Issue) -> Dict[str, Any]:
        """Generate operation for outliers"""
        col = issue.column
        outlier_pct = issue.affected_percentage

        # Use capping for low percentage outliers, remove for high
        strategy = 'remove' if outlier_pct > 5 else 'cap'

        return {
            'column': col,
            'operation': 'handle_outliers',
            'parameters': {
                'strategy': strategy,
            }
        }

    @staticmethod
    def _handle_rare_categories_rule(df: pd.DataFrame, issue: Issue) -> Dict[str, Any]:
        """Generate operation for rare categories"""
        return {
            'column': issue.column,
            'operation': 'group_rare_categories',
            'parameters': {
                'threshold': 0.01,
                'group_label': 'Other'
            }
        }

    @staticmethod
    def validate_operation(operation: Dict[str, Any], df: pd.DataFrame) -> bool:
        """Validate if operation is safe to apply"""
        column = operation.get('column')
        op_type = operation.get('operation')

        if column == 'all':
            return True

        if column not in df.columns:
            return False

        # Add safety checks for specific operations
        if op_type == 'handle_outliers':
            if not np.issubdtype(df[column].dtype, np.number):
                return False

        if op_type == 'impute_missing':
            if df[column].isnull().sum() == 0:
                return False  # No missing values to impute

        return True
