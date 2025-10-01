from typing import List, Dict, Any
from datetime import datetime, timedelta
from statistics import mean
from ..models.health_recovery import SleepData, RecoveryMetrics, HealthMetrics
from ..schemas.health import HealthInsightsResponse, HealthTrend, HealthInsight

def calculate_recovery_score(metrics: Dict[str, Any]) -> int:
    """
    Calculate overall recovery score based on various metrics.
    
    Weights:
    - HRV: 30%
    - Sleep quality: 25%
    - Resting heart rate: 20%
    - Previous activity: 15%
    - Stress level: 10%
    """
    weights = {
        'hrv': 0.30,
        'sleep': 0.25,
        'resting_hr': 0.20,
        'activity': 0.15,
        'stress': 0.10
    }
    
    scores = {
        'hrv': normalize_hrv(metrics.get('hrv', 0)),
        'sleep': metrics.get('sleep_quality', 0),
        'resting_hr': normalize_heart_rate(metrics.get('resting_heart_rate', 60)),
        'activity': normalize_activity(metrics.get('previous_activity', 0)),
        'stress': 100 - metrics.get('stress_level', 0)  # Invert stress level
    }
    
    weighted_score = sum(scores[key] * weights[key] for key in weights)
    return round(weighted_score)

def normalize_hrv(hrv_value: float) -> float:
    """Normalize HRV value to a 0-100 scale."""
    # These thresholds should be adjusted based on user demographics
    MIN_HRV = 20
    MAX_HRV = 100
    
    normalized = ((hrv_value - MIN_HRV) / (MAX_HRV - MIN_HRV)) * 100
    return max(0, min(100, normalized))

def normalize_heart_rate(hr_value: int) -> float:
    """Normalize resting heart rate to a 0-100 scale."""
    # These thresholds should be adjusted based on user demographics
    OPTIMAL_HR_RANGE = (55, 65)
    MAX_DEVIATION = 30
    
    if OPTIMAL_HR_RANGE[0] <= hr_value <= OPTIMAL_HR_RANGE[1]:
        return 100
    
    deviation = min(
        abs(hr_value - OPTIMAL_HR_RANGE[0]),
        abs(hr_value - OPTIMAL_HR_RANGE[1])
    )
    
    score = max(0, 100 - (deviation / MAX_DEVIATION) * 100)
    return score

def normalize_activity(activity_score: float) -> float:
    """Normalize activity level to a 0-100 scale."""
    return max(0, min(100, activity_score))

def generate_health_insights(
    metrics: List[HealthMetrics],
    recovery_data: List[RecoveryMetrics],
    sleep_data: List[SleepData]
) -> HealthInsightsResponse:
    """Generate comprehensive health insights based on all available data."""
    
    # Calculate overall health score
    recent_recovery = [m.readiness_score for m in recovery_data[-7:]]
    recent_sleep = [s.sleep_score for s in sleep_data[-7:]]
    
    overall_score = round(mean([
        mean(recent_recovery) if recent_recovery else 0,
        mean(recent_sleep) if recent_sleep else 0
    ]))
    
    # Analyze trends
    trends = []
    metrics_by_type = {}
    for metric in metrics:
        if metric.metric_type not in metrics_by_type:
            metrics_by_type[metric.metric_type] = []
        metrics_by_type[metric.metric_type].append(metric)
    
    for metric_type, metric_data in metrics_by_type.items():
        if len(metric_data) >= 2:
            current = metric_data[-1].value
            previous = metric_data[-2].value
            change = ((current - previous) / previous) * 100
            
            trends.append(HealthTrend(
                metric=metric_type,
                trend="improving" if change > 0 else "declining",
                change_percentage=abs(change),
                is_positive=is_positive_trend(metric_type, change)
            ))
    
    # Generate insights
    insights = []
    
    # Sleep insights
    if sleep_data:
        avg_sleep = mean([s.duration for s in sleep_data[-7:]])
        if avg_sleep < 7:
            insights.append(HealthInsight(
                category="sleep",
                title="Insufficient Sleep",
                description=f"Average sleep duration of {avg_sleep:.1f} hours is below recommended levels",
                severity="high",
                recommendations=[
                    "Aim for 7-9 hours of sleep per night",
                    "Maintain a consistent sleep schedule",
                    "Create a relaxing bedtime routine"
                ]
            ))
    
    # Recovery insights
    if recovery_data:
        recent_strain = [m.muscle_strain for m in recovery_data[-3:]]
        if mean(recent_strain) > 80:
            insights.append(HealthInsight(
                category="recovery",
                title="High Physical Strain",
                description="Sustained high physical strain detected",
                severity="medium",
                recommendations=[
                    "Schedule a recovery day",
                    "Focus on light activities",
                    "Increase focus on mobility work"
                ]
            ))
    
    return HealthInsightsResponse(
        overall_health_score=overall_score,
        trends=trends,
        insights=insights,
        last_updated=datetime.utcnow()
    )

def process_device_data(data: Dict[str, Any], device_type: str) -> List[Dict[str, Any]]:
    """Process and normalize data from different device types."""
    processed_data = []
    
    if device_type == "smartwatch":
        # Process smartwatch data
        for record in data.get('activities', []):
            processed_data.append({
                'timestamp': record.get('timestamp'),
                'heart_rate': record.get('heart_rate'),
                'steps': record.get('steps'),
                'activity_type': record.get('type'),
                'duration': record.get('duration'),
                'calories': record.get('calories')
            })
    
    elif device_type == "sleep_tracker":
        # Process sleep tracker data
        for record in data.get('sleep_sessions', []):
            processed_data.append({
                'date': record.get('date'),
                'duration': record.get('duration'),
                'deep_sleep': record.get('deep_sleep'),
                'rem_sleep': record.get('rem_sleep'),
                'light_sleep': record.get('light_sleep'),
                'awake_time': record.get('awake')
            })
    
    return processed_data

def analyze_health_trends(metrics_data: List[HealthMetrics]) -> Dict[str, Any]:
    """Analyze health metrics data to identify trends and patterns."""
    trends = {}
    
    # Group metrics by type
    metrics_by_type = {}
    for metric in metrics_data:
        if metric.metric_type not in metrics_by_type:
            metrics_by_type[metric.metric_type] = []
        metrics_by_type[metric.metric_type].append(metric)
    
    # Analyze each metric type
    for metric_type, data in metrics_by_type.items():
        values = [m.value for m in sorted(data, key=lambda x: x.date)]
        dates = [m.date for m in sorted(data, key=lambda x: x.date)]
        
        trends[metric_type] = {
            'values': values,
            'dates': dates,
            'trend_direction': calculate_trend_direction(values),
            'min_value': min(values),
            'max_value': max(values),
            'average': mean(values),
            'variability': calculate_variability(values)
        }
    
    return trends

def calculate_trend_direction(values: List[float]) -> str:
    """Calculate the overall trend direction of a series of values."""
    if len(values) < 2:
        return "stable"
    
    # Calculate simple linear regression slope
    n = len(values)
    x = list(range(n))
    mean_x = mean(x)
    mean_y = mean(values)
    
    numerator = sum((x[i] - mean_x) * (values[i] - mean_y) for i in range(n))
    denominator = sum((x[i] - mean_x) ** 2 for i in range(n))
    
    if denominator == 0:
        return "stable"
    
    slope = numerator / denominator
    
    if slope > 0.05:
        return "increasing"
    elif slope < -0.05:
        return "decreasing"
    else:
        return "stable"

def calculate_variability(values: List[float]) -> float:
    """Calculate the coefficient of variation for a series of values."""
    if not values:
        return 0
    
    avg = mean(values)
    if avg == 0:
        return 0
    
    std_dev = (sum((x - avg) ** 2 for x in values) / len(values)) ** 0.5
    return (std_dev / avg) * 100

def is_positive_trend(metric_type: str, change: float) -> bool:
    """Determine if a trend is positive based on the metric type."""
    # Metrics where an increase is positive
    positive_increase = {
        'hrv',
        'sleep_duration',
        'deep_sleep_percentage',
        'recovery_score',
        'strength_score'
    }
    
    # Metrics where a decrease is positive
    positive_decrease = {
        'resting_heart_rate',
        'stress_level',
        'body_fat_percentage',
        'recovery_time'
    }
    
    if metric_type in positive_increase:
        return change > 0
    elif metric_type in positive_decrease:
        return change < 0
    
    return True  # Default to positive for unknown metrics