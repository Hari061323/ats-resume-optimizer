"""
AI ATS Scorer
Calculates comprehensive ATS scores with detailed analysis
"""

import json
import re
import os
from typing import Dict, Any, List, Tuple
import requests
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
# Look for .env in parent directory (project root)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OpenAIClient:
    """OpenAI client using the official library"""
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key not found in environment variables")
        
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)
        except ImportError:
            logger.error("OpenAI library not installed. Please install with: pip install openai")
            raise
    
    def chat_completion(self, messages: List[Dict], model: str = "gpt-3.5-turbo", 
                       temperature: float = 0.7, max_tokens: int = 2000) -> Dict:
        """Make a chat completion request to OpenAI"""
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return {
                'choices': [{
                    'message': {
                        'content': response.choices[0].message.content
                    }
                }]
            }
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise


class AIATSScorer:
    """Calculate ATS score with detailed breakdown"""
    
    def __init__(self):
        self.client = OpenAIClient()
        
        # Scoring weights
        self.weights = {
            'keyword_match': 0.35,      # 35%
            'skills_alignment': 0.20,    # 20%
            'experience_relevance': 0.15,# 15%
            'format_compatibility': 0.15,# 15%
            'achievements_impact': 0.10, # 10%
            'completeness': 0.05         # 5%
        }
        
        # Grade mapping
        self.grade_map = {
            (90, 100): 'A+',
            (85, 89): 'A',
            (80, 84): 'B+',
            (75, 79): 'B',
            (70, 74): 'B-',
            (65, 69): 'C+',
            (60, 64): 'C',
            (0, 59): 'D'
        }
    
    def calculate_score(self, resume_data: Dict, job_analysis: Dict, 
                       keyword_match: Dict) -> Dict[str, Any]:
        """Calculate comprehensive ATS score"""
        
        # Calculate individual component scores
        scores = {
            'keyword_match': self._score_keywords(keyword_match),
            'skills_alignment': self._score_skills(resume_data, job_analysis),
            'experience_relevance': self._score_experience(resume_data, job_analysis),
            'format_compatibility': self._score_format(resume_data),
            'achievements_impact': self._score_achievements(resume_data),
            'completeness': self._score_completeness(resume_data)
        }
        
        # Calculate weighted total
        total_score = sum(scores[key] * self.weights[key] for key in scores)
        
        # Get grade
        grade = self._get_grade(total_score)
        
        # Generate SWOT analysis
        swot = self._generate_swot(resume_data, job_analysis, scores)
        
        # Generate improvement roadmap
        improvements = self._generate_improvements(scores, resume_data, job_analysis)
        
        # AI-powered insights
        ai_insights = self._get_ai_insights(resume_data, job_analysis, scores)
        
        return {
            'total_score': round(total_score, 2),
            'grade': grade,
            'component_scores': scores,
            'weighted_scores': {k: round(v * self.weights[k], 2) for k, v in scores.items()},
            'swot_analysis': swot,
            'improvement_roadmap': improvements,
            'ai_insights': ai_insights,
            'pass_probability': self._calculate_pass_probability(total_score),
            'competitive_rating': self._get_competitive_rating(total_score),
            'timestamp': datetime.now().isoformat()
        }
    
    def _score_keywords(self, keyword_match: Dict) -> float:
        """Score keyword matching"""
        match_percentage = keyword_match.get('match_percentage', 0)
        
        # Bonus for optimal keyword density
        density = keyword_match.get('keyword_density', 0)
        density_bonus = 10 if 2 <= density <= 5 else 0
        
        # Semantic match bonus
        semantic_count = len(keyword_match.get('semantic_matches', []))
        semantic_bonus = min(semantic_count * 2, 10)
        
        score = match_percentage + density_bonus + semantic_bonus
        return min(score, 100)
    
    def _score_skills(self, resume_data: Dict, job_analysis: Dict) -> float:
        """Score skills alignment"""
        resume_skills = set()
        for skill_type in resume_data.get('skills', {}).values():
            if isinstance(skill_type, list):
                resume_skills.update([s.lower() for s in skill_type])
        
        required_skills = set([s.lower() for s in job_analysis.get('required_skills', [])])
        
        if not required_skills:
            return 75  # Default score
        
        matched_skills = resume_skills & required_skills
        match_rate = len(matched_skills) / len(required_skills)
        
        # Bonus for extra relevant skills
        extra_skills = len(resume_skills - required_skills)
        skill_bonus = min(extra_skills * 2, 20)
        
        return min(match_rate * 80 + skill_bonus, 100)
    
    def _score_experience(self, resume_data: Dict, job_analysis: Dict) -> float:
        """Score experience relevance"""
        required_years = job_analysis.get('experience_years', 0)
        actual_years = resume_data.get('meta', {}).get('total_experience_years', 0)
        
        if required_years == 0:
            return 85  # Default if no requirement specified
        
        # Calculate match
        if actual_years >= required_years:
            base_score = 90
            # Small bonus for exceeding requirements
            excess_bonus = min((actual_years - required_years) * 2, 10)
            score = base_score + excess_bonus
        else:
            # Penalty for not meeting requirements
            deficit_penalty = (required_years - actual_years) * 15
            score = max(90 - deficit_penalty, 20)
        
        # Check for relevant job titles
        job_level = job_analysis.get('job_level', '').lower()
        for exp in resume_data.get('experience', []):
            if job_level in exp.get('title', '').lower():
                score = min(score + 10, 100)
                break
        
        return score
    
    def _score_format(self, resume_data: Dict) -> float:
        """Score format and ATS compatibility"""
        score = 100
        
        # Check for contact information
        contact = resume_data.get('contact', {})
        if not contact.get('email'):
            score -= 20
        if not contact.get('phone'):
            score -= 10
        
        # Check for proper sections
        if not resume_data.get('experience'):
            score -= 25
        if not resume_data.get('education'):
            score -= 15
        if not resume_data.get('skills'):
            score -= 20
        
        # Bonus for clean structure
        if resume_data.get('summary'):
            score += 5
        
        # Check for parsing success
        if resume_data.get('meta', {}).get('skill_count', 0) > 0:
            score += 5
        
        return max(min(score, 100), 0)
    
    def _score_achievements(self, resume_data: Dict) -> float:
        """Score achievements and quantification"""
        has_metrics = resume_data.get('meta', {}).get('has_quantified_achievements', False)
        
        if has_metrics:
            base_score = 80
        else:
            base_score = 40
        
        # Count total achievements
        achievement_count = 0
        for exp in resume_data.get('experience', []):
            achievement_count += len(exp.get('achievements', []))
        
        # Bonus for multiple achievements
        achievement_bonus = min(achievement_count * 5, 20)
        
        return min(base_score + achievement_bonus, 100)
    
    def _score_completeness(self, resume_data: Dict) -> float:
        """Score resume completeness"""
        sections = ['contact', 'summary', 'experience', 'education', 
                   'skills', 'projects', 'certifications']
        
        completed = sum(1 for section in sections if resume_data.get(section))
        completeness_score = (completed / len(sections)) * 100
        
        # Bonus for additional sections
        if resume_data.get('awards') or resume_data.get('publications'):
            completeness_score = min(completeness_score + 10, 100)
        
        return completeness_score
    
    def _get_grade(self, score: float) -> str:
        """Convert score to letter grade"""
        for (min_score, max_score), grade in self.grade_map.items():
            if min_score <= score <= max_score:
                return grade
        return 'D'
    
    def _generate_swot(self, resume_data: Dict, job_analysis: Dict, 
                      scores: Dict) -> Dict[str, List[str]]:
        """Generate SWOT analysis"""
        swot = {
            'strengths': [],
            'weaknesses': [],
            'opportunities': [],
            'threats': []
        }
        
        # Strengths
        if scores['keyword_match'] >= 80:
            swot['strengths'].append('Strong keyword alignment with job requirements')
        if scores['achievements_impact'] >= 80:
            swot['strengths'].append('Excellent quantified achievements')
        if resume_data.get('meta', {}).get('project_count', 0) > 2:
            swot['strengths'].append('Strong project portfolio demonstrating practical skills')
        
        # Weaknesses
        if scores['keyword_match'] < 60:
            swot['weaknesses'].append('Low keyword match - may not pass initial ATS screening')
        if not resume_data.get('summary'):
            swot['weaknesses'].append('Missing professional summary')
        if scores['achievements_impact'] < 50:
            swot['weaknesses'].append('Lack of quantified achievements')
        
        # Opportunities
        swot['opportunities'].append('Add industry-specific certifications')
        swot['opportunities'].append('Include more metrics and KPIs in experience descriptions')
        if not resume_data.get('projects'):
            swot['opportunities'].append('Add relevant projects section')
        
        # Threats
        if scores['experience_relevance'] < 60:
            swot['threats'].append('Experience level may not match job requirements')
        if scores['format_compatibility'] < 70:
            swot['threats'].append('Format issues may cause ATS parsing errors')
        
        return swot
    
    def _generate_improvements(self, scores: Dict, resume_data: Dict, 
                              job_analysis: Dict) -> List[Dict[str, Any]]:
        """Generate prioritized improvement roadmap"""
        improvements = []
        
        # Analyze each component for improvements
        for component, score in scores.items():
            if score < 80:
                improvement = {
                    'component': component,
                    'current_score': score,
                    'target_score': 90,
                    'priority': 'High' if score < 60 else 'Medium',
                    'actions': []
                }
                
                if component == 'keyword_match':
                    improvement['actions'] = [
                        'Add missing keywords naturally throughout resume',
                        'Use job description terminology',
                        'Include industry-specific terms'
                    ]
                elif component == 'skills_alignment':
                    improvement['actions'] = [
                        'Add relevant technical skills',
                        'Organize skills by category',
                        'Include proficiency levels'
                    ]
                elif component == 'achievements_impact':
                    improvement['actions'] = [
                        'Quantify all achievements with metrics',
                        'Use CAR (Challenge-Action-Result) format',
                        'Add percentage improvements, dollar amounts'
                    ]
                
                improvements.append(improvement)
        
        # Sort by priority
        improvements.sort(key=lambda x: 0 if x['priority'] == 'High' else 1)
        
        return improvements[:5]  # Top 5 improvements
    
    def _get_ai_insights(self, resume_data: Dict, job_analysis: Dict, 
                        scores: Dict) -> Dict[str, Any]:
        """Get AI-powered insights about the resume"""
        
        prompt = f"""Analyze this resume scoring data and provide strategic insights:
        
        Scores: {json.dumps(scores, indent=2)}
        Experience Years: {resume_data.get('meta', {}).get('total_experience_years', 0)}
        Required Years: {job_analysis.get('experience_years', 0)}
        Has Quantified Achievements: {resume_data.get('meta', {}).get('has_quantified_achievements', False)}
        
        Provide:
        1. Main strength of this resume
        2. Critical weakness that needs immediate attention
        3. Quick win improvement (can be done in 15 minutes)
        4. Strategic recommendation for this candidate
        5. Predicted interview probability (percentage)"""
        
        messages = [
            {"role": "system", "content": "You are an expert ATS analyst and career coach."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = self.client.chat_completion(messages, temperature=0.5, max_tokens=500)
            content = response['choices'][0]['message']['content']
            
            # Parse insights
            insights = {
                'main_strength': '',
                'critical_weakness': '',
                'quick_win': '',
                'strategic_recommendation': '',
                'interview_probability': 0
            }
            
            # Simple parsing (you might want to make this more robust)
            lines = content.split('\n')
            for line in lines:
                if '1.' in line or 'strength' in line.lower():
                    insights['main_strength'] = line.split(':', 1)[-1].strip()
                elif '2.' in line or 'weakness' in line.lower():
                    insights['critical_weakness'] = line.split(':', 1)[-1].strip()
                elif '3.' in line or 'quick win' in line.lower():
                    insights['quick_win'] = line.split(':', 1)[-1].strip()
                elif '4.' in line or 'strategic' in line.lower():
                    insights['strategic_recommendation'] = line.split(':', 1)[-1].strip()
                elif '5.' in line or 'probability' in line.lower():
                    # Extract percentage
                    import re
                    match = re.search(r'(\d+)%?', line)
                    if match:
                        insights['interview_probability'] = int(match.group(1))
            
            return insights
            
        except Exception as e:
            logger.error(f"Error getting AI insights: {str(e)}")
            return {
                'main_strength': 'Unable to analyze',
                'critical_weakness': 'Unable to analyze',
                'quick_win': 'Add more keywords from job description',
                'strategic_recommendation': 'Focus on quantifying achievements',
                'interview_probability': 50
            }
    
    def _calculate_pass_probability(self, score: float) -> str:
        """Calculate probability of passing ATS"""
        if score >= 85:
            return 'Very High (90%+)'
        elif score >= 75:
            return 'High (70-90%)'
        elif score >= 65:
            return 'Medium (50-70%)'
        elif score >= 55:
            return 'Low (30-50%)'
        else:
            return 'Very Low (<30%)'
    
    def _get_competitive_rating(self, score: float) -> str:
        """Get competitive rating compared to other candidates"""
        if score >= 90:
            return 'Top 10% of candidates'
        elif score >= 80:
            return 'Top 25% of candidates'
        elif score >= 70:
            return 'Top 50% of candidates'
        elif score >= 60:
            return 'Bottom 50% of candidates'
        else:
            return 'Needs significant improvement'