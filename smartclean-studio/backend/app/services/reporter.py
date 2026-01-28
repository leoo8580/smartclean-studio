from typing import List, Dict, Any
from models.schemas import CleaningOperation, QualityScore, CleaningResult


class Reporter:
    """Generates cleaning reports and explanations"""

    @staticmethod
    def generate_report(
        cleaned_data: List[Dict[str, Any]],
        operations_applied: List[CleaningOperation],
        quality_before: QualityScore,
        quality_after: QualityScore,
        processing_time_ms: float
    ) -> Dict[str, Any]:
        """Generate comprehensive cleaning report"""
        
        issues_resolved = len(operations_applied)
        improvement_pct = quality_after.overall - quality_before.overall

        report = {
            'summary': {
                'total_operations': len(operations_applied),
                'issues_resolved': issues_resolved,
                'quality_improvement': round(improvement_pct, 1),
                'processing_time_ms': round(processing_time_ms, 1),
                'before_score': round(quality_before.overall, 1),
                'after_score': round(quality_after.overall, 1)
            },
            'quality_comparison': {
                'completeness': {
                    'before': round(quality_before.completeness, 1),
                    'after': round(quality_after.completeness, 1),
                    'improvement': round(quality_after.completeness - quality_before.completeness, 1)
                },
                'uniqueness': {
                    'before': round(quality_before.uniqueness, 1),
                    'after': round(quality_after.uniqueness, 1),
                    'improvement': round(quality_after.uniqueness - quality_before.uniqueness, 1)
                },
                'consistency': {
                    'before': round(quality_before.consistency, 1),
                    'after': round(quality_after.consistency, 1),
                    'improvement': round(quality_after.consistency - quality_before.consistency, 1)
                },
                'accuracy': {
                    'before': round(quality_before.accuracy, 1),
                    'after': round(quality_after.accuracy, 1),
                    'improvement': round(quality_after.accuracy - quality_before.accuracy, 1)
                }
            },
            'operations': [Reporter._format_operation(op) for op in operations_applied]
        }

        return report

    @staticmethod
    def _format_operation(operation: CleaningOperation) -> Dict[str, Any]:
        """Format operation for human-readable report"""
        return {
            'column': operation.column,
            'operation': operation.operation_type,
            'description': operation.description,
            'rows_affected': operation.rows_affected,
            'applied_by': operation.applied_by,
            'technical_details': operation.parameters
        }

    @staticmethod
    def get_human_readable_report(report: Dict[str, Any]) -> str:
        """Generate human-readable text report"""
        summary = report['summary']
        quality = report['quality_comparison']

        text = f"""
SMARTCLEAN STUDIO - DATA CLEANING REPORT
{'='*60}

SUMMARY
{'-'*60}
Total Operations Applied: {summary['total_operations']}
Issues Resolved: {summary['issues_resolved']}
Quality Improvement: +{summary['quality_improvement']}%
Processing Time: {summary['processing_time_ms']}ms

QUALITY SCORES
{'-'*60}
Overall Score: {summary['before_score']} → {summary['after_score']} (+{summary['quality_improvement']}%)

Completeness:  {quality['completeness']['before']}% → {quality['completeness']['after']}% (+{quality['completeness']['improvement']}%)
Uniqueness:    {quality['uniqueness']['before']}% → {quality['uniqueness']['after']}% (+{quality['uniqueness']['improvement']}%)
Consistency:   {quality['consistency']['before']}% → {quality['consistency']['after']}% (+{quality['consistency']['improvement']}%)
Accuracy:      {quality['accuracy']['before']}% → {quality['accuracy']['after']}% (+{quality['accuracy']['improvement']}%)

CLEANING OPERATIONS APPLIED
{'-'*60}
"""
        for i, op in enumerate(report['operations'], 1):
            text += f"""
{i}. {op['column'].upper()}
   Operation: {op['operation']}
   Description: {op['description']}
   Rows Affected: {op['rows_affected']}
   Applied By: {op['applied_by']}
"""
        
        return text
