"""
Analytics Dashboard for AI Resume Optimizer
Provides comprehensive analytics, tracking, and insights
"""

import json
import os
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime, timedelta
from collections import defaultdict
import hashlib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AnalyticsDashboard:
    """
    Comprehensive analytics dashboard for resume optimization
    Features:
    1. User session tracking
    2. Score analytics and trends
    3. Performance metrics
    4. Improvement tracking
    5. Comparative analysis
    6. Success metrics
    """
    
    def __init__(self):
        # Reduced debug output for faster initialization
        self.analytics_data = {}
        self.user_sessions = {}
        self.score_history = defaultdict(list)
        self.performance_metrics = defaultdict(int)
        
        # Create analytics directory
        self.analytics_dir = os.path.join(os.path.dirname(__file__), 'analytics')
        os.makedirs(self.analytics_dir, exist_ok=True)
        
        # Load existing data
        self._load_analytics_data()
    
    def track_analysis(self, user_id: str, analysis_data: Dict, job_title: str = None) -> str:
        """Track a new analysis session"""
        
        analysis_id = self._generate_analysis_id(user_id, analysis_data)
        timestamp = datetime.now()
        
        # Create session data
        session_data = {
            'analysis_id': analysis_id,
            'user_id': user_id,
            'timestamp': timestamp.isoformat(),
            'job_title': job_title,
            'scores': self._extract_scores(analysis_data),
            'improvements': self._extract_improvements(analysis_data),
            'enhancement_level': analysis_data.get('enhancement_level', 'moderate'),
            'file_size': analysis_data.get('file_size', 0),
            'processing_time': analysis_data.get('processing_time', 0)
        }
        
        # Store session
        self.user_sessions[analysis_id] = session_data
        
        # Update score history
        if 'overall_score' in analysis_data:
            self.score_history[user_id].append({
                'timestamp': timestamp.isoformat(),
                'score': analysis_data['overall_score'],
                'analysis_id': analysis_id,
                'job_title': job_title
            })
        
        # Update performance metrics
        self._update_performance_metrics(session_data)
        
        # Save data
        self._save_analytics_data()
        
        return analysis_id
    
    def get_user_dashboard(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive dashboard for a user"""
        
        user_sessions = [session for session in self.user_sessions.values() 
                        if session['user_id'] == user_id]
        
        if not user_sessions:
            return self._get_empty_dashboard()
        
        # Sort by timestamp
        user_sessions.sort(key=lambda x: x['timestamp'], reverse=True)
        
        # Calculate metrics
        total_analyses = len(user_sessions)
        latest_score = user_sessions[0]['scores'].get('overall_score', 0)
        score_trend = self._calculate_score_trend(user_id)
        improvement_rate = self._calculate_improvement_rate(user_id)
        
        # Get recent analyses
        recent_analyses = user_sessions[:5]
        
        # Get score distribution
        score_distribution = self._get_score_distribution(user_sessions)
        
        # Get improvement areas
        improvement_areas = self._get_improvement_areas(user_sessions)
        
        # Get job title analysis
        job_analysis = self._get_job_title_analysis(user_sessions)
        
        return {
            'user_id': user_id,
            'total_analyses': total_analyses,
            'latest_score': latest_score,
            'score_trend': score_trend,
            'improvement_rate': improvement_rate,
            'recent_analyses': recent_analyses,
            'score_distribution': score_distribution,
            'improvement_areas': improvement_areas,
            'job_analysis': job_analysis,
            'performance_insights': self._get_performance_insights(user_sessions),
            'recommendations': self._get_user_recommendations(user_sessions),
            'timestamp': datetime.now().isoformat()
        }
    
    def get_system_analytics(self) -> Dict[str, Any]:
        """Get system-wide analytics"""
        
        total_users = len(set(session['user_id'] for session in self.user_sessions.values()))
        total_analyses = len(self.user_sessions)
        
        # Calculate average scores
        all_scores = [session['scores'].get('overall_score', 0) 
                     for session in self.user_sessions.values()]
        avg_score = sum(all_scores) / len(all_scores) if all_scores and len(all_scores) > 0 else 0
        
        # Get score distribution
        score_ranges = {
            'A+ (90-100)': len([s for s in all_scores if 90 <= s <= 100]),
            'A (85-89)': len([s for s in all_scores if 85 <= s <= 89]),
            'B+ (80-84)': len([s for s in all_scores if 80 <= s <= 84]),
            'B (75-79)': len([s for s in all_scores if 75 <= s <= 79]),
            'Below B (<75)': len([s for s in all_scores if s < 75])
        }
        
        # Get popular job titles
        job_titles = [session.get('job_title', 'Unknown') 
                     for session in self.user_sessions.values()]
        popular_jobs = self._get_popular_jobs(job_titles)
        
        # Get enhancement level usage
        enhancement_levels = [session.get('enhancement_level', 'moderate') 
                            for session in self.user_sessions.values()]
        enhancement_usage = self._get_enhancement_usage(enhancement_levels)
        
        # Get performance metrics
        avg_processing_time = sum(session.get('processing_time', 0) 
                                for session in self.user_sessions.values()) / total_analyses if total_analyses > 0 else 0
        
        return {
            'total_users': total_users,
            'total_analyses': total_analyses,
            'average_score': round(avg_score, 2),
            'score_distribution': score_ranges,
            'popular_job_titles': popular_jobs,
            'enhancement_level_usage': enhancement_usage,
            'average_processing_time': round(avg_processing_time, 2),
            'performance_metrics': dict(self.performance_metrics),
            'system_health': self._get_system_health(),
            'timestamp': datetime.now().isoformat()
        }
    
    def get_score_analytics(self, user_id: str = None) -> Dict[str, Any]:
        """Get detailed score analytics"""
        
        if user_id:
            sessions = [session for session in self.user_sessions.values() 
                       if session['user_id'] == user_id]
        else:
            sessions = list(self.user_sessions.values())
        
        if not sessions:
            return {'error': 'No data available'}
        
        # Extract all scores
        all_scores = []
        component_scores = defaultdict(list)
        
        for session in sessions:
            scores = session.get('scores', {})
            if 'overall_score' in scores:
                all_scores.append(scores['overall_score'])
            
            for component, score in scores.items():
                if component != 'overall_score':
                    component_scores[component].append(score)
        
        # Calculate statistics
        score_stats = {
            'count': len(all_scores),
            'mean': round(sum(all_scores) / len(all_scores), 2) if all_scores and len(all_scores) > 0 else 0,
            'median': round(sorted(all_scores)[len(all_scores)//2], 2) if all_scores and len(all_scores) > 0 else 0,
            'min': min(all_scores) if all_scores else 0,
            'max': max(all_scores) if all_scores else 0,
            'std_dev': self._calculate_std_dev(all_scores) if all_scores and len(all_scores) > 0 else 0
        }
        
        # Component analysis
        component_analysis = {}
        for component, scores in component_scores.items():
            if scores and len(scores) > 0:
                component_analysis[component] = {
                    'average': round(sum(scores) / len(scores), 2),
                    'count': len(scores),
                    'trend': self._calculate_trend(scores)
                }
        
        return {
            'score_statistics': score_stats,
            'component_analysis': component_analysis,
            'score_trend': self._calculate_score_trend(user_id) if user_id else None,
            'improvement_areas': self._get_improvement_areas(sessions),
            'timestamp': datetime.now().isoformat()
        }
    
    def get_improvement_tracking(self, user_id: str) -> Dict[str, Any]:
        """Track improvement progress over time"""
        
        user_sessions = [session for session in self.user_sessions.values() 
                        if session['user_id'] == user_id]
        
        if len(user_sessions) < 2:
            return {'error': 'Need at least 2 analyses to track improvement'}
        
        # Sort by timestamp
        user_sessions.sort(key=lambda x: x['timestamp'])
        
        # Calculate improvement metrics
        first_score = user_sessions[0]['scores'].get('overall_score', 0)
        latest_score = user_sessions[-1]['scores'].get('overall_score', 0)
        total_improvement = latest_score - first_score
        
        # Calculate improvement rate
        time_span = (datetime.fromisoformat(user_sessions[-1]['timestamp']) - 
                    datetime.fromisoformat(user_sessions[0]['timestamp'])).days
        improvement_rate = total_improvement / max(time_span, 1)
        
        # Get improvement timeline
        improvement_timeline = []
        for i, session in enumerate(user_sessions):
            if i > 0:
                prev_score = user_sessions[i-1]['scores'].get('overall_score', 0)
                current_score = session['scores'].get('overall_score', 0)
                improvement = current_score - prev_score
                
                improvement_timeline.append({
                    'timestamp': session['timestamp'],
                    'score': current_score,
                    'improvement': improvement,
                    'analysis_id': session['analysis_id']
                })
        
        # Get improvement areas
        improvement_areas = self._get_improvement_areas(user_sessions)
        
        return {
            'total_improvement': round(total_improvement, 2),
            'improvement_rate': round(improvement_rate, 2),
            'first_score': first_score,
            'latest_score': latest_score,
            'improvement_timeline': improvement_timeline,
            'improvement_areas': improvement_areas,
            'recommendations': self._get_improvement_recommendations(user_sessions),
            'timestamp': datetime.now().isoformat()
        }
    
    def _generate_analysis_id(self, user_id: str, analysis_data: Dict) -> str:
        """Generate unique analysis ID"""
        content = f"{user_id}_{analysis_data.get('timestamp', '')}_{datetime.now().isoformat()}"
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def _extract_scores(self, analysis_data: Dict) -> Dict[str, float]:
        """Extract scores from analysis data"""
        scores = {}
        
        if 'overall_score' in analysis_data:
            scores['overall_score'] = analysis_data['overall_score']
        
        if 'component_scores' in analysis_data:
            scores.update(analysis_data['component_scores'])
        
        return scores
    
    def _extract_improvements(self, analysis_data: Dict) -> List[str]:
        """Extract improvement recommendations"""
        improvements = []
        
        if 'improvement_recommendations' in analysis_data:
            recs = analysis_data['improvement_recommendations']
            if isinstance(recs, list):
                improvements.extend(recs)
            elif isinstance(recs, dict) and 'priority_recommendations' in recs:
                improvements.extend([rec.get('recommendation', '') for rec in recs['priority_recommendations']])
        
        return improvements
    
    def _calculate_score_trend(self, user_id: str) -> str:
        """Calculate score trend for user"""
        scores = self.score_history.get(user_id, [])
        if len(scores) < 2:
            return 'insufficient_data'
        
        recent_scores = scores[-5:]  # Last 5 scores
        if len(recent_scores) < 2:
            return 'insufficient_data'
        
        first_score = recent_scores[0]['score']
        last_score = recent_scores[-1]['score']
        
        if last_score > first_score + 5:
            return 'improving'
        elif last_score < first_score - 5:
            return 'declining'
        else:
            return 'stable'
    
    def _calculate_improvement_rate(self, user_id: str) -> float:
        """Calculate improvement rate for user"""
        scores = self.score_history.get(user_id, [])
        if len(scores) < 2:
            return 0.0
        
        first_score = scores[0]['score']
        last_score = scores[-1]['score']
        
        return round(last_score - first_score, 2)
    
    def _get_score_distribution(self, sessions: List[Dict]) -> Dict[str, int]:
        """Get score distribution for sessions"""
        distribution = {
            'A+ (90-100)': 0,
            'A (85-89)': 0,
            'B+ (80-84)': 0,
            'B (75-79)': 0,
            'Below B (<75)': 0
        }
        
        for session in sessions:
            score = session['scores'].get('overall_score', 0)
            if 90 <= score <= 100:
                distribution['A+ (90-100)'] += 1
            elif 85 <= score <= 89:
                distribution['A (85-89)'] += 1
            elif 80 <= score <= 84:
                distribution['B+ (80-84)'] += 1
            elif 75 <= score <= 79:
                distribution['B (75-79)'] += 1
            else:
                distribution['Below B (<75)'] += 1
        
        return distribution
    
    def _get_improvement_areas(self, sessions: List[Dict]) -> List[Dict]:
        """Get common improvement areas"""
        improvement_counts = defaultdict(int)
        
        for session in sessions:
            improvements = session.get('improvements', [])
            for improvement in improvements:
                improvement_counts[improvement] += 1
        
        # Sort by frequency
        sorted_improvements = sorted(improvement_counts.items(), 
                                   key=lambda x: x[1], reverse=True)
        
        return [{'area': area, 'frequency': count} 
                for area, count in sorted_improvements[:5]]
    
    def _get_job_title_analysis(self, sessions: List[Dict]) -> Dict[str, Any]:
        """Analyze job titles for user"""
        job_titles = [session.get('job_title', 'Unknown') for session in sessions]
        job_counts = defaultdict(int)
        
        for job in job_titles:
            job_counts[job] += 1
        
        most_common = max(job_counts.items(), key=lambda x: x[1]) if job_counts else ('Unknown', 0)
        
        return {
            'most_common_job': most_common[0],
            'job_frequency': most_common[1],
            'total_job_types': len(job_counts),
            'job_distribution': dict(job_counts)
        }
    
    def _get_performance_insights(self, sessions: List[Dict]) -> Dict[str, Any]:
        """Get performance insights for user"""
        if not sessions:
            return {}
        
        avg_processing_time = sum(s.get('processing_time', 0) for s in sessions) / len(sessions) if sessions else 0
        avg_file_size = sum(s.get('file_size', 0) for s in sessions) / len(sessions) if sessions else 0
        
        return {
            'average_processing_time': round(avg_processing_time, 2),
            'average_file_size': round(avg_file_size, 2),
            'total_sessions': len(sessions),
            'enhancement_preference': self._get_most_used_enhancement_level(sessions)
        }
    
    def _get_user_recommendations(self, sessions: List[Dict]) -> List[str]:
        """Get personalized recommendations for user"""
        recommendations = []
        
        if not sessions:
            return recommendations
        
        latest_session = sessions[0]
        latest_score = latest_session['scores'].get('overall_score', 0)
        
        if latest_score < 70:
            recommendations.append("Focus on improving overall resume structure and content quality")
        elif latest_score < 85:
            recommendations.append("Work on enhancing specific sections to reach A-level scores")
        else:
            recommendations.append("Maintain current quality and focus on job-specific optimization")
        
        # Add specific recommendations based on improvement areas
        improvement_areas = self._get_improvement_areas(sessions)
        if improvement_areas:
            top_area = improvement_areas[0]['area']
            recommendations.append(f"Priority: Address {top_area} for better results")
        
        return recommendations
    
    def _get_popular_jobs(self, job_titles: List[str]) -> List[Dict]:
        """Get popular job titles"""
        job_counts = defaultdict(int)
        for job in job_titles:
            job_counts[job] += 1
        
        sorted_jobs = sorted(job_counts.items(), key=lambda x: x[1], reverse=True)
        return [{'job_title': job, 'count': count} for job, count in sorted_jobs[:10]]
    
    def _get_enhancement_usage(self, enhancement_levels: List[str]) -> Dict[str, int]:
        """Get enhancement level usage statistics"""
        usage = defaultdict(int)
        for level in enhancement_levels:
            usage[level] += 1
        return dict(usage)
    
    def _get_system_health(self) -> Dict[str, Any]:
        """Get system health metrics"""
        return {
            'total_sessions': len(self.user_sessions),
            'active_users': len(set(session['user_id'] for session in self.user_sessions.values())),
            'data_integrity': 'good',
            'last_updated': datetime.now().isoformat()
        }
    
    def _calculate_std_dev(self, scores: List[float]) -> float:
        """Calculate standard deviation"""
        if len(scores) < 2:
            return 0.0
        
        mean = sum(scores) / len(scores)
        variance = sum((x - mean) ** 2 for x in scores) / len(scores)
        return round(variance ** 0.5, 2)
    
    def _calculate_trend(self, scores: List[float]) -> str:
        """Calculate trend for a list of scores"""
        if len(scores) < 2:
            return 'stable'
        
        first_half = scores[:len(scores)//2]
        second_half = scores[len(scores)//2:]
        
        first_avg = sum(first_half) / len(first_half)
        second_avg = sum(second_half) / len(second_half)
        
        if second_avg > first_avg + 2:
            return 'improving'
        elif second_avg < first_avg - 2:
            return 'declining'
        else:
            return 'stable'
    
    def _get_most_used_enhancement_level(self, sessions: List[Dict]) -> str:
        """Get most used enhancement level"""
        levels = [s.get('enhancement_level', 'moderate') for s in sessions]
        level_counts = defaultdict(int)
        for level in levels:
            level_counts[level] += 1
        
        return max(level_counts.items(), key=lambda x: x[1])[0] if level_counts else 'moderate'
    
    def _get_improvement_recommendations(self, sessions: List[Dict]) -> List[str]:
        """Get improvement recommendations based on session history"""
        recommendations = []
        
        if len(sessions) < 2:
            return ["Continue using the system to track improvement over time"]
        
        # Analyze score progression
        scores = [s['scores'].get('overall_score', 0) for s in sessions]
        if scores[-1] > scores[0]:
            recommendations.append("Great progress! Continue with current improvement strategy")
        else:
            recommendations.append("Consider trying different enhancement levels or focusing on specific areas")
        
        return recommendations
    
    def _update_performance_metrics(self, session_data: Dict):
        """Update performance metrics"""
        self.performance_metrics['total_analyses'] += 1
        self.performance_metrics['total_processing_time'] += session_data.get('processing_time', 0)
        self.performance_metrics['total_file_size'] += session_data.get('file_size', 0)
    
    def _get_empty_dashboard(self) -> Dict[str, Any]:
        """Get empty dashboard for new users"""
        return {
            'user_id': 'new_user',
            'total_analyses': 0,
            'latest_score': 0,
            'score_trend': 'no_data',
            'improvement_rate': 0,
            'recent_analyses': [],
            'score_distribution': {},
            'improvement_areas': [],
            'job_analysis': {},
            'performance_insights': {},
            'recommendations': ['Start by uploading your first resume for analysis'],
            'timestamp': datetime.now().isoformat()
        }
    
    def _load_analytics_data(self):
        """Load analytics data from file"""
        try:
            data_file = os.path.join(self.analytics_dir, 'analytics_data.json')
            if os.path.exists(data_file):
                with open(data_file, 'r') as f:
                    data = json.load(f)
                    self.user_sessions = data.get('user_sessions', {})
                    self.score_history = defaultdict(list, data.get('score_history', {}))
                    self.performance_metrics = defaultdict(int, data.get('performance_metrics', {}))
        except Exception as e:
            logger.error(f"Error loading analytics data: {str(e)}")
    
    def _save_analytics_data(self):
        """Save analytics data to file"""
        try:
            data_file = os.path.join(self.analytics_dir, 'analytics_data.json')
            data = {
                'user_sessions': self.user_sessions,
                'score_history': dict(self.score_history),
                'performance_metrics': dict(self.performance_metrics),
                'last_updated': datetime.now().isoformat()
            }
            with open(data_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving analytics data: {str(e)}")
