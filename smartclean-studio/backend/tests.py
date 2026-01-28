"""
SmartClean Studio - Test Suite

This file contains tests to verify the application works correctly.
Run with: pytest tests/test_cleaning.py
"""

# Import test dependencies if running tests
# pytest, pytest-asyncio should be installed

def test_imports():
    """Test that all modules can be imported"""
    from app.models.schemas import DatasetInfo, QualityScore, Issue
    from app.services.analyzer import DataAnalyzer
    from app.services.cleaner import DataCleaner
    from app.services.rule_engine import RuleEngine
    from app.services.reporter import Reporter
    assert True

def test_quality_score_calculation():
    """Test quality score calculations"""
    from app.services.analyzer import DataAnalyzer
    import pandas as pd
    
    df = pd.DataFrame({
        'A': [1, 2, 3, 4, 5],
        'B': ['x', 'y', 'z', 'x', 'y'],
        'C': [10.5, 20.3, 30.1, 40.2, 50.4]
    })
    
    analyzer = DataAnalyzer(df, 'test.csv', 1.0)
    score = analyzer._calculate_quality_score()
    
    assert 0 <= score.completeness <= 100
    assert 0 <= score.uniqueness <= 100
    assert 0 <= score.consistency <= 100
    assert 0 <= score.accuracy <= 100
    assert 0 <= score.overall <= 100

def test_missing_value_detection():
    """Test detection of missing values"""
    from app.services.analyzer import DataAnalyzer
    import pandas as pd
    
    df = pd.DataFrame({
        'A': [1, 2, None, 4, 5],
        'B': ['x', None, 'z', 'x', 'y']
    })
    
    analyzer = DataAnalyzer(df, 'test.csv', 1.0)
    issues = analyzer._detect_issues()
    
    # Should detect missing values in both columns
    missing_issues = [i for i in issues if i.issue_type.value == 'missing_values']
    assert len(missing_issues) >= 2

def test_outlier_detection():
    """Test detection of outliers"""
    from app.services.analyzer import DataAnalyzer
    import pandas as pd
    
    df = pd.DataFrame({
        'values': [1, 2, 3, 4, 5, 6, 7, 8, 9, 100]  # 100 is outlier
    })
    
    analyzer = DataAnalyzer(df, 'test.csv', 1.0)
    issues = analyzer._detect_issues()
    
    # Should detect outlier
    outlier_issues = [i for i in issues if i.issue_type.value == 'outliers']
    assert len(outlier_issues) > 0

def test_data_cleaner():
    """Test data cleaning operations"""
    from app.services.cleaner import DataCleaner
    import pandas as pd
    
    df = pd.DataFrame({
        'A': [1, 2, None, 4, 5],
        'B': [10, 200, 30, 40, 50]  # 200 is potential outlier
    })
    
    cleaner = DataCleaner(df)
    
    # Test imputation
    operations = [
        {
            'column': 'A',
            'operation': 'impute_missing',
            'parameters': {'strategy': 'mean'}
        }
    ]
    
    cleaned_df = cleaner.apply_operations(operations)
    
    # Check that no values are NaN after cleaning
    assert cleaned_df['A'].isna().sum() == 0

if __name__ == '__main__':
    print("Running SmartClean Studio tests...")
    
    try:
        test_imports()
        print("✓ Imports test passed")
    except Exception as e:
        print(f"✗ Imports test failed: {e}")
    
    try:
        test_quality_score_calculation()
        print("✓ Quality score test passed")
    except Exception as e:
        print(f"✗ Quality score test failed: {e}")
    
    try:
        test_missing_value_detection()
        print("✓ Missing value detection test passed")
    except Exception as e:
        print(f"✗ Missing value detection test failed: {e}")
    
    try:
        test_outlier_detection()
        print("✓ Outlier detection test passed")
    except Exception as e:
        print(f"✗ Outlier detection test failed: {e}")
    
    try:
        test_data_cleaner()
        print("✓ Data cleaner test passed")
    except Exception as e:
        print(f"✗ Data cleaner test failed: {e}")
    
    print("\nAll tests completed!")
