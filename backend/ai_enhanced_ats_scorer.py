"""
Enhanced AI ATS Scorer with Project Learning Integration
Combines traditional ATS scoring with advanced project-based learning analysis
"""

import json
import re
import os
from typing import Dict, Any, List, Tuple
import logging
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

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
    
    def chat_completion(self, messages: List[Dict], model: str = "gpt-4", 
                       temperature: float = 0.3, max_tokens: int = 2000) -> Dict:
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

class AIEnhancedATSScorer:
    """
    Enhanced ATS Scorer that combines:
    1. Traditional ATS scoring (keywords, format, etc.)
    2. Project-based learning analysis
    3. Experience relevance scoring
    4. AI-powered insights and recommendations
    """
    
    def __init__(self):
        self.client = OpenAIClient()
        
        # Import the project learning scorer
        try:
            from ai_project_learning_scorer import AIProjectLearningScorer
            self.project_scorer = AIProjectLearningScorer()
        except ImportError:
            logger.warning("Project learning scorer not available, using basic scoring")
            self.project_scorer = None
        
        # Enhanced scoring weights
        self.weights = {
            'keyword_match': 0.25,          # 25% - Traditional keyword matching
            'project_learning': 0.30,       # 30% - Project-based learning analysis
            'experience_relevance': 0.20,   # 20% - Experience alignment
            'skills_alignment': 0.15,       # 15% - Skills matching
            'format_compatibility': 0.10    # 10% - ATS format compatibility
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
    
    def calculate_enhanced_score(self, resume_data: Dict, job_analysis: Dict, 
                                keyword_match: Dict) -> Dict[str, Any]:
        """
        Calculate comprehensive enhanced ATS score
        """
        
        # Calculate individual component scores
        scores = {
            'keyword_match': self._score_keywords(keyword_match),
            'project_learning': self._score_project_learning(resume_data, job_analysis),
            'experience_relevance': self._score_experience_relevance(resume_data, job_analysis),
            'skills_alignment': self._score_skills_alignment(resume_data, job_analysis),
            'format_compatibility': self._score_format_compatibility(resume_data)
        }
        
        # Calculate weighted total
        total_score = sum(scores[key] * self.weights[key] for key in scores)
        
        # Get grade
        grade = self._get_grade(total_score)
        
        # Generate comprehensive analysis
        analysis = self._generate_comprehensive_analysis(resume_data, job_analysis, scores, keyword_match)
        
        # Generate learning-based recommendations
        recommendations = self._generate_learning_recommendations(resume_data, job_analysis, scores)
        
        return {
            'total_score': round(total_score, 2),
            'grade': grade,
            'component_scores': scores,
            'weighted_scores': {k: round(v * self.weights[k], 2) for k, v in scores.items()},
            'analysis': analysis,
            'recommendations': recommendations,
            'learning_path': self._generate_learning_path(resume_data, job_analysis, scores),
            'pass_probability': self._calculate_pass_probability(total_score),
            'competitive_rating': self._get_competitive_rating(total_score),
            'timestamp': datetime.now().isoformat()
        }
    
    def _score_keywords(self, keyword_match: Dict) -> float:
        """Score keyword matching (traditional ATS)"""
        match_percentage = keyword_match.get('match_percentage', 0)
        
        # Bonus for optimal keyword density
        density = keyword_match.get('keyword_density', 0)
        density_bonus = 10 if 2 <= density <= 5 else 0
        
        # Semantic match bonus
        semantic_count = len(keyword_match.get('semantic_matches', []))
        semantic_bonus = min(semantic_count * 2, 10)
        
        score = match_percentage + density_bonus + semantic_bonus
        return min(score, 100)
    
    def _score_project_learning(self, resume_data: Dict, job_analysis: Dict) -> float:
        """Score project-based learning using AI analysis"""
        if not self.project_scorer:
            # Fallback to basic project scoring
            projects = resume_data.get('projects', [])
            if not projects:
                return 20
            return min(len(projects) * 20, 100)
        
        try:
            project_score = self.project_scorer.calculate_project_score(resume_data, job_analysis)
            return project_score['total_score']
        except Exception as e:
            logger.error(f"Error in project learning scorer: {str(e)}")
            # Fallback scoring
            projects = resume_data.get('projects', [])
            return min(len(projects) * 25, 100) if projects else 20
    
    def _score_experience_relevance(self, resume_data: Dict, job_analysis: Dict) -> float:
        """Score experience relevance with AI analysis"""
        
        # Basic experience scoring
        required_years = job_analysis.get('experience_years', 0)
        actual_years = resume_data.get('meta', {}).get('total_experience_years', 0)
        
        if required_years == 0:
            base_score = 85
        elif actual_years >= required_years:
            base_score = 90
            excess_bonus = min((actual_years - required_years) * 2, 10)
            base_score += excess_bonus
        else:
            deficit_penalty = (required_years - actual_years) * 15
            base_score = max(90 - deficit_penalty, 20)
        
        # AI-powered experience analysis
        experience_analysis = self._analyze_experience_with_ai(resume_data, job_analysis)
        
        # Adjust score based on AI analysis
        if experience_analysis.get('relevance_score', 0) > 80:
            base_score = min(base_score + 10, 100)
        elif experience_analysis.get('relevance_score', 0) < 50:
            base_score = max(base_score - 15, 20)
        
        return base_score
    
    def _score_skills_alignment(self, resume_data: Dict, job_analysis: Dict) -> float:
        """Score skills alignment with job requirements"""
        resume_skills = set()
        for skill_type in resume_data.get('skills', {}).values():
            if isinstance(skill_type, list):
                resume_skills.update([s.lower() for s in skill_type])
        
        required_skills = set([s.lower() for s in job_analysis.get('required_skills', [])])
        
        if not required_skills:
            return 75
        
        matched_skills = resume_skills & required_skills
        match_rate = len(matched_skills) / len(required_skills)
        
        # Bonus for extra relevant skills
        extra_skills = len(resume_skills - required_skills)
        skill_bonus = min(extra_skills * 2, 20)
        
        return min(match_rate * 80 + skill_bonus, 100)
    
    def _score_format_compatibility(self, resume_data: Dict) -> float:
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
        
        return max(min(score, 100), 0)
    
    def _analyze_experience_with_ai(self, resume_data: Dict, job_analysis: Dict) -> Dict:
        """Use AI to analyze experience relevance"""
        
        experience = resume_data.get('experience', [])
        job_description = job_analysis.get('description', '')
        job_title = job_analysis.get('title', '')
        
        if not experience:
            return {'relevance_score': 0, 'analysis': 'No experience found'}
        
        prompt = f"""
        Analyze the relevance of this work experience for a {job_title} position:
        
        Job Description: {job_description[:300]}...
        
        Experience: {json.dumps(experience, indent=2)}
        
        Analyze:
        1. How relevant is each role to the target position?
        2. What transferable skills are demonstrated?
        3. How does the career progression align with the job requirements?
        4. What gaps exist between current experience and job requirements?
        
        Return as JSON:
        {{
            "relevance_score": 85,
            "role_analysis": [
                {{
                    "title": "role_title",
                    "relevance": "high/medium/low",
                    "transferable_skills": ["skill1", "skill2"],
                    "alignment_score": 80
                }}
            ],
            "career_progression": "description",
            "transferable_skills": ["skill1", "skill2"],
            "gaps": ["gap1", "gap2"],
            "strengths": ["strength1", "strength2"]
        }}
        """
        
        messages = [
            {"role": "system", "content": "You are an expert career advisor. Analyze work experience for job relevance and career alignment."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = self.client.chat_completion(messages, temperature=0.3, max_tokens=1000)
            content = response['choices'][0]['message']['content']
            
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return {'relevance_score': 60, 'analysis': 'Standard experience analysis'}
                
        except Exception as e:
            logger.error(f"Error analyzing experience with AI: {str(e)}")
            return {'relevance_score': 60, 'analysis': 'Fallback analysis'}
    
    def _generate_comprehensive_analysis(self, resume_data: Dict, job_analysis: Dict, 
                                       scores: Dict, keyword_match: Dict) -> Dict:
        """Generate comprehensive analysis combining all scoring components"""
        
        analysis = {
            'overall_assessment': '',
            'strengths': [],
            'weaknesses': [],
            'project_insights': {},
            'experience_insights': {},
            'skill_gaps': [],
            'improvement_areas': [],
            'career_alignment': ''
        }
        
        # Overall assessment
        total_score = sum(scores[key] * self.weights[key] for key in scores)
        if total_score >= 85:
            analysis['overall_assessment'] = 'Excellent match - strong candidate with relevant experience and skills'
        elif total_score >= 70:
            analysis['overall_assessment'] = 'Good match - solid foundation with some areas for improvement'
        elif total_score >= 55:
            analysis['overall_assessment'] = 'Moderate match - potential candidate with significant gaps to address'
        else:
            analysis['overall_assessment'] = 'Weak match - major improvements needed to be competitive'
        
        # Strengths
        if scores['project_learning'] >= 80:
            analysis['strengths'].append('Strong project portfolio demonstrating practical skills')
        if scores['experience_relevance'] >= 80:
            analysis['strengths'].append('Relevant work experience aligned with job requirements')
        if scores['skills_alignment'] >= 80:
            analysis['strengths'].append('Excellent skills match with job requirements')
        if scores['keyword_match'] >= 80:
            analysis['strengths'].append('Strong keyword alignment for ATS systems')
        
        # Weaknesses
        if scores['project_learning'] < 60:
            analysis['weaknesses'].append('Limited or weak project portfolio')
        if scores['experience_relevance'] < 60:
            analysis['weaknesses'].append('Experience not well-aligned with job requirements')
        if scores['skills_alignment'] < 60:
            analysis['weaknesses'].append('Skills gap with job requirements')
        if scores['keyword_match'] < 60:
            analysis['weaknesses'].append('Poor keyword match - may not pass ATS screening')
        
        # Project insights (if available)
        if self.project_scorer:
            try:
                project_score = self.project_scorer.calculate_project_score(resume_data, job_analysis)
                analysis['project_insights'] = project_score.get('insights', {})
            except Exception as e:
                logger.error(f"Error getting project insights: {str(e)}")
        
        # Experience insights
        experience_analysis = self._analyze_experience_with_ai(resume_data, job_analysis)
        analysis['experience_insights'] = experience_analysis
        
        # Skill gaps
        resume_skills = set()
        for skill_type in resume_data.get('skills', {}).values():
            if isinstance(skill_type, list):
                resume_skills.update([s.lower() for s in skill_type])
        
        required_skills = set([s.lower() for s in job_analysis.get('required_skills', [])])
        missing_skills = required_skills - resume_skills
        analysis['skill_gaps'] = list(missing_skills)[:5]
        
        return analysis
    
    def _generate_learning_recommendations(self, resume_data: Dict, job_analysis: Dict, scores: Dict) -> List[str]:
        """Generate personalized learning recommendations"""
        
        recommendations = []
        
        # Project-based recommendations
        if scores['project_learning'] < 70:
            recommendations.append('Build more relevant projects that demonstrate job-specific skills')
            recommendations.append('Focus on projects that solve real-world problems in your target industry')
        
        # Experience recommendations
        if scores['experience_relevance'] < 70:
            recommendations.append('Highlight transferable skills from your current experience')
            recommendations.append('Consider taking on projects or responsibilities that align with your target role')
        
        # Skills recommendations
        if scores['skills_alignment'] < 70:
            missing_skills = job_analysis.get('required_skills', [])[:3]
            recommendations.append(f'Learn and practice: {", ".join(missing_skills)}')
        
        # Keyword recommendations
        if scores['keyword_match'] < 70:
            recommendations.append('Incorporate more job-relevant keywords naturally throughout your resume')
            recommendations.append('Use the exact terminology from the job description')
        
        # General recommendations
        recommendations.extend([
            'Document your learning journey and skill development',
            'Create a portfolio showcasing your best work',
            'Get feedback from industry professionals',
            'Stay updated with latest trends in your field'
        ])
        
        return recommendations[:6]  # Top 6 recommendations
    
    def _generate_learning_path(self, resume_data: Dict, job_analysis: Dict, scores: Dict) -> Dict:
        """Generate a personalized learning path"""
        
        learning_path = {
            'immediate_actions': [],
            'short_term_goals': [],
            'long_term_goals': [],
            'resources': [],
            'timeline': '3-6 months'
        }
        
        # Immediate actions (1-2 weeks)
        if scores['keyword_match'] < 70:
            learning_path['immediate_actions'].append('Optimize resume with job-relevant keywords')
        if scores['format_compatibility'] < 80:
            learning_path['immediate_actions'].append('Fix resume formatting and structure')
        
        # Short-term goals (1-3 months)
        if scores['project_learning'] < 70:
            learning_path['short_term_goals'].append('Complete 2-3 relevant projects')
        if scores['skills_alignment'] < 70:
            learning_path['short_term_goals'].append('Learn missing technical skills')
        
        # Long-term goals (3-6 months)
        learning_path['long_term_goals'].extend([
            'Build a comprehensive portfolio',
            'Gain relevant work experience or internships',
            'Develop expertise in target technologies'
        ])
        
        # Resources
        learning_path['resources'].extend([
            'Online courses (Coursera, Udemy, edX)',
            'Technical documentation and tutorials',
            'Open source projects and contributions',
            'Professional networking and mentorship'
        ])
        
        return learning_path
    
    def _get_grade(self, score: float) -> str:
        """Convert score to letter grade"""
        for (min_score, max_score), grade in self.grade_map.items():
            if min_score <= score <= max_score:
                return grade
        return 'D'
    
    def _calculate_pass_probability(self, score: float) -> str:
        """Calculate probability of passing ATS screening"""
        if score >= 85:
            return 'Very High (90%+)'
        elif score >= 75:
            return 'High (75-90%)'
        elif score >= 65:
            return 'Moderate (50-75%)'
        elif score >= 55:
            return 'Low (25-50%)'
        else:
            return 'Very Low (<25%)'
    
    def _get_competitive_rating(self, score: float) -> str:
        """Get competitive rating"""
        if score >= 85:
            return 'Top 10% of candidates'
        elif score >= 75:
            return 'Top 25% of candidates'
        elif score >= 65:
            return 'Above average'
        elif score >= 55:
            return 'Average'
        else:
            return 'Below average'
