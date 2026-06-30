from datetime import datetime


def get_source_quarter():
    """
    Returns the current source quarter.
    Example:
        2026-Q1
        2026-Q2
        2026-Q3
        2026-Q4
    """
    current_date = datetime.now()

    year = current_date.year
    quarter = ((current_date.month - 1) // 3) + 1

    return f"{year}-Q{quarter}"


def get_pipeline_timestamp():
    """
    Returns the current pipeline execution timestamp.
    Example:
        2026-07-01 10:45:32
    """
    return datetime.now()