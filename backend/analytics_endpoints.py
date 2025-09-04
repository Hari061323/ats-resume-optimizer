"""
Analytics API Endpoints for AI Resume Optimizer
Provides comprehensive analytics and tracking capabilities
"""

from fastapi import APIRouter, HTTPException, Depends, Query, Body
from typing import Dict, Any, Optional, List
import logging
from datetime import datetime, timedelta
from analytics_dashboard import AnalyticsDashboard

logger = logging.getLogger(__name__)

# Create router for analytics endpoints
analytics_router = APIRouter(prefix="/analytics", tags=["Analytics"])

# Initialize analytics dashboard
analytics_dashboard = AnalyticsDashboard()

@analytics_router.get("/dashboard/{user_id}")
async def get_user_dashboard(user_id: str):
    """Get comprehensive analytics dashboard for a user"""
    try:
        dashboard_data = analytics_dashboard.get_user_dashboard(user_id)
        return {
            'success': True,
            'data': dashboard_data
        }
    except Exception as e:
        logger.error(f"Error getting user dashboard: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@analytics_router.get("/system")
async def get_system_analytics():
    """Get system-wide analytics"""
    try:
        system_data = analytics_dashboard.get_system_analytics()
        return {
            'success': True,
            'data': system_data
        }
    except Exception as e:
        logger.error(f"Error getting system analytics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@analytics_router.get("/scores/{user_id}")
async def get_score_analytics(user_id: str):
    """Get detailed score analytics for a user"""
    try:
        score_data = analytics_dashboard.get_score_analytics(user_id)
        return {
            'success': True,
            'data': score_data
        }
    except Exception as e:
        logger.error(f"Error getting score analytics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@analytics_router.get("/improvement/{user_id}")
async def get_improvement_tracking(user_id: str):
    """Track improvement progress over time"""
    try:
        improvement_data = analytics_dashboard.get_improvement_tracking(user_id)
        return {
            'success': True,
            'data': improvement_data
        }
    except Exception as e:
        logger.error(f"Error getting improvement tracking: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@analytics_router.get("/scores")
async def get_global_score_analytics():
    """Get global score analytics across all users"""
    try:
        score_data = analytics_dashboard.get_score_analytics()
        return {
            'success': True,
            'data': score_data
        }
    except Exception as e:
        logger.error(f"Error getting global score analytics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@analytics_router.get("/trends/{user_id}")
async def get_user_trends(
    user_id: str,
    days: int = Query(30, description="Number of days to analyze")
):
    """Get user trends over specified time period"""
    try:
        # Get user sessions within time period
        cutoff_date = datetime.now() - timedelta(days=days)
        
        user_sessions = [
            session for session in analytics_dashboard.user_sessions.values()
            if (session['user_id'] == user_id and 
                datetime.fromisoformat(session['timestamp']) >= cutoff_date)
        ]
        
        if not user_sessions:
            return {
                'success': True,
                'data': {
                    'error': f'No data available for the last {days} days',
                    'user_id': user_id,
                    'days_analyzed': days
                }
            }
        
        # Calculate trends
        scores = [session['scores'].get('overall_score', 0) for session in user_sessions]
        avg_score = sum(scores) / len(scores) if scores else 0
        
        # Calculate trend direction
        if len(scores) >= 2:
            first_half = scores[:len(scores)//2]
            second_half = scores[len(scores)//2:]
            trend = 'improving' if sum(second_half)/len(second_half) > sum(first_half)/len(first_half) else 'declining'
        else:
            trend = 'insufficient_data'
        
        return {
            'success': True,
            'data': {
                'user_id': user_id,
                'days_analyzed': days,
                'total_analyses': len(user_sessions),
                'average_score': round(avg_score, 2),
                'trend_direction': trend,
                'score_range': {
                    'min': min(scores) if scores else 0,
                    'max': max(scores) if scores else 0
                },
                'recent_scores': scores[-10:] if len(scores) > 10 else scores
            }
        }
    except Exception as e:
        logger.error(f"Error getting user trends: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@analytics_router.get("/performance")
async def get_performance_metrics():
    """Get system performance metrics"""
    try:
        system_data = analytics_dashboard.get_system_analytics()
        
        performance_data = {
            'total_analyses': system_data.get('total_analyses', 0),
            'total_users': system_data.get('total_users', 0),
            'average_processing_time': system_data.get('average_processing_time', 0),
            'average_score': system_data.get('average_score', 0),
            'system_health': system_data.get('system_health', {}),
            'performance_metrics': system_data.get('performance_metrics', {}),
            'timestamp': datetime.now().isoformat()
        }
        
        return {
            'success': True,
            'data': performance_data
        }
    except Exception as e:
        logger.error(f"Error getting performance metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@analytics_router.get("/insights/{user_id}")
async def get_user_insights(user_id: str):
    """Get personalized insights and recommendations for a user"""
    try:
        dashboard_data = analytics_dashboard.get_user_dashboard(user_id)
        
        insights = {
            'user_id': user_id,
            'key_insights': [],
            'recommendations': dashboard_data.get('recommendations', []),
            'improvement_areas': dashboard_data.get('improvement_areas', []),
            'performance_insights': dashboard_data.get('performance_insights', {}),
            'score_trend': dashboard_data.get('score_trend', 'no_data'),
            'improvement_rate': dashboard_data.get('improvement_rate', 0)
        }
        
        # Generate key insights
        latest_score = dashboard_data.get('latest_score', 0)
        total_analyses = dashboard_data.get('total_analyses', 0)
        
        if latest_score >= 90:
            insights['key_insights'].append("Excellent resume quality! You're in the top tier of candidates.")
        elif latest_score >= 80:
            insights['key_insights'].append("Good resume quality with room for targeted improvements.")
        elif latest_score >= 70:
            insights['key_insights'].append("Solid foundation with significant improvement potential.")
        else:
            insights['key_insights'].append("Focus on fundamental improvements to boost your resume quality.")
        
        if total_analyses > 1:
            improvement_rate = dashboard_data.get('improvement_rate', 0)
            if improvement_rate > 5:
                insights['key_insights'].append(f"Great progress! You've improved by {improvement_rate} points.")
            elif improvement_rate > 0:
                insights['key_insights'].append(f"Steady improvement of {improvement_rate} points.")
            else:
                insights['key_insights'].append("Consider trying different enhancement strategies.")
        
        return {
            'success': True,
            'data': insights
        }
    except Exception as e:
        logger.error(f"Error getting user insights: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@analytics_router.get("/comparison/{user_id}")
async def get_comparative_analysis(user_id: str):
    """Get comparative analysis against other users"""
    try:
        user_dashboard = analytics_dashboard.get_user_dashboard(user_id)
        system_analytics = analytics_dashboard.get_system_analytics()
        
        user_score = user_dashboard.get('latest_score', 0)
        system_avg = system_analytics.get('average_score', 0)
        
        comparison = {
            'user_id': user_id,
            'user_score': user_score,
            'system_average': system_avg,
            'percentile': 0,
            'comparison': 'average',
            'insights': []
        }
        
        # Calculate percentile
        if system_avg > 0:
            if user_score > system_avg + 10:
                comparison['percentile'] = 90
                comparison['comparison'] = 'excellent'
                comparison['insights'].append("You're performing significantly above average!")
            elif user_score > system_avg + 5:
                comparison['percentile'] = 75
                comparison['comparison'] = 'above_average'
                comparison['insights'].append("You're performing above average.")
            elif user_score > system_avg - 5:
                comparison['percentile'] = 50
                comparison['comparison'] = 'average'
                comparison['insights'].append("You're performing at the average level.")
            else:
                comparison['percentile'] = 25
                comparison['comparison'] = 'below_average'
                comparison['insights'].append("There's significant room for improvement.")
        
        return {
            'success': True,
            'data': comparison
        }
    except Exception as e:
        logger.error(f"Error getting comparative analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@analytics_router.post("/track")
async def track_analysis(
    user_id: str = Query(...),
    job_title: Optional[str] = Query(None),
    analysis_data: Dict[str, Any] = Body(...)
):
    """Track a new analysis session"""
    try:
        analysis_id = analytics_dashboard.track_analysis(user_id, analysis_data, job_title)
        return {
            'success': True,
            'analysis_id': analysis_id,
            'message': 'Analysis tracked successfully'
        }
    except Exception as e:
        logger.error(f"Error tracking analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@analytics_router.get("/health")
async def get_analytics_health():
    """Get analytics system health status"""
    try:
        health_data = {
            'status': 'healthy',
            'total_sessions': len(analytics_dashboard.user_sessions),
            'active_users': len(set(session['user_id'] for session in analytics_dashboard.user_sessions.values())),
            'last_updated': datetime.now().isoformat(),
            'data_integrity': 'good'
        }
        
        return {
            'success': True,
            'data': health_data
        }
    except Exception as e:
        logger.error(f"Error getting analytics health: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
