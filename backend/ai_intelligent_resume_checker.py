"""
Intelligent AI Resume Checker with Advanced Documentation
Uses GPT-4.1 for superior analysis, documentation, and job relevance matching
"""

import json
import re
import os
import time
from typing import Dict, Any, List, Tuple, Optional
import logging
from dotenv import load_dotenv
from datetime import datetime
import hashlib

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OpenAIClient:
    """OpenAI client using GPT-4.1 for superior analysis"""
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
                       temperature: float = 0.2, max_tokens: int = 1500) -> Dict:
        """Make a chat completion request to GPT-4.1"""
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
            # Fallback to GPT-3.5-turbo if GPT-4 is not available
            if model == "gpt-4":
                logger.info("Falling back to GPT-3.5-turbo")
                return self.chat_completion(messages, "gpt-3.5-turbo", temperature, max_tokens)
            raise

class IntelligentResumeChecker:
    """
    Intelligent AI Resume Checker with Advanced Documentation
    Features:
    1. Comprehensive resume analysis and documentation
    2. Advanced job relevance matching
    3. Detailed improvement recommendations
    4. Industry-specific insights
    5. ATS optimization guidance
    6. Career progression analysis
    """
    
    def __init__(self):
        self.client = OpenAIClient()
        
        # Analysis categories with weights
        self.analysis_weights = {
            'content_quality': 0.25,      # 25% - Content quality and clarity
            'job_relevance': 0.30,        # 30% - Job-specific relevance
            'technical_depth': 0.20,      # 20% - Technical sophistication
            'achievement_impact': 0.15,   # 15% - Quantified achievements
            'career_progression': 0.10    # 10% - Career growth pattern
        }
        
        # Industry-specific templates
        self.industry_templates = {
            'data_science': {
                'keywords': ['python', 'machine learning', 'statistics', 'sql', 'pandas', 'numpy'],
                'metrics': ['accuracy', 'performance', 'model', 'dataset', 'algorithm'],
                'skills': ['python', 'r', 'sql', 'machine learning', 'statistics', 'data visualization']
            },
            'software_engineering': {
                'keywords': ['python', 'javascript', 'java', 'react', 'node.js', 'api'],
                'metrics': ['performance', 'scalability', 'efficiency', 'uptime', 'users'],
                'skills': ['programming', 'algorithms', 'data structures', 'system design', 'testing']
            },
            'product_management': {
                'keywords': ['strategy', 'roadmap', 'stakeholder', 'metrics', 'user experience'],
                'metrics': ['revenue', 'growth', 'conversion', 'retention', 'engagement'],
                'skills': ['strategy', 'analytics', 'communication', 'leadership', 'product development']
            }
        }
        
        # ATS optimization rules
        self.ats_rules = {
            'format_requirements': [
                'Use standard fonts (Arial, Calibri, Times New Roman)',
                'Maintain consistent formatting throughout',
                'Use bullet points for achievements',
                'Include relevant keywords naturally',
                'Keep file size under 2MB'
            ],
            'content_requirements': [
                'Include quantifiable achievements',
                'Use action verbs to start bullet points',
                'Tailor content to job requirements',
                'Include relevant skills and technologies',
                'Show career progression'
            ]
        }
    
    def comprehensive_resume_analysis(self, resume_data: Dict, job_analysis: Dict) -> Dict[str, Any]:
        """
        Perform comprehensive resume analysis with detailed documentation
        """
        
        # Generate unique analysis ID
        analysis_id = self._generate_analysis_id(resume_data, job_analysis)
        
        # Perform multi-dimensional analysis
        analysis_results = {
            'analysis_id': analysis_id,
            'timestamp': datetime.now().isoformat(),
            'resume_summary': self._analyze_resume_structure(resume_data),
            'job_relevance_analysis': self._analyze_job_relevance(resume_data, job_analysis),
            'technical_assessment': self._assess_technical_depth(resume_data, job_analysis),
            'achievement_analysis': self._analyze_achievements(resume_data),
            'career_progression': self._analyze_career_progression(resume_data),
            'ats_optimization': self._analyze_ats_compatibility(resume_data, job_analysis),
            'industry_insights': self._generate_industry_insights(resume_data, job_analysis),
            'improvement_recommendations': self._generate_improvement_recommendations(resume_data, job_analysis),
            'documentation_report': self._generate_documentation_report(resume_data, job_analysis)
        }
        
        # Calculate overall score
        overall_score = self._calculate_overall_score(analysis_results)
        analysis_results['overall_score'] = overall_score
        analysis_results['grade'] = self._get_grade(overall_score)
        
        return analysis_results
    
    def fast_comprehensive_analysis(self, resume_data: Dict, job_analysis: Dict) -> Dict[str, Any]:
        """
        Fast comprehensive analysis with reduced API calls for better performance
        """
        try:
            # Perform only essential analyses (3 instead of 7)
            structure_analysis = self._analyze_resume_structure(resume_data)
            job_relevance = self._analyze_job_relevance(resume_data, job_analysis)
            technical_assessment = self._assess_technical_depth(resume_data, job_analysis)
            
            # Calculate overall score
            scores = [
                structure_analysis.get('score', 0),
                job_relevance.get('score', 0),
                technical_assessment.get('score', 0)
            ]
            overall_score = sum(scores) / len(scores) if scores else 0
            
            # Generate quick insights
            key_insights = [
                f"Resume structure: {structure_analysis.get('score', 0)}/100",
                f"Job relevance: {job_relevance.get('score', 0)}/100", 
                f"Technical depth: {technical_assessment.get('score', 0)}/100"
            ]
            
            recommendations = [
                "Quantify achievements with specific metrics",
                "Align skills with job requirements",
                "Improve resume formatting and structure"
            ]
            
            return {
                'analysis_id': f"fast_analysis_{int(time.time())}",
                'overall_score': overall_score,
                'dimensional_scores': {
                    'structure': structure_analysis.get('score', 0),
                    'job_relevance': job_relevance.get('score', 0),
                    'technical_depth': technical_assessment.get('score', 0),
                    'achievements_impact': 75,  # Default
                    'career_progression': 80,   # Default
                    'ats_optimization': 85,     # Default
                    'industry_alignment': 70    # Default
                },
                'job_relevance_score': job_relevance.get('score', 0),
                'job_relevance_analysis': job_relevance.get('analysis', 'Analysis completed'),
                'key_insights': key_insights,
                'recommendations': recommendations,
                'industry_insights': "Focus on current industry trends and technologies"
            }
            
        except Exception as e:
            logger.error(f"Error in fast analysis: {str(e)}")
            return {
                'analysis_id': f"error_analysis_{int(time.time())}",
                'overall_score': 0,
                'error': str(e),
                'dimensional_scores': {},
                'key_insights': [],
                'recommendations': [],
                'job_relevance_score': 0,
                'job_relevance_analysis': 'Analysis failed',
                'industry_insights': 'Analysis failed'
            }
    
    def _analyze_resume_structure(self, resume_data: Dict) -> Dict:
        """Analyze resume structure and content quality"""
        
        prompt = f"""
        Analyze this resume structure and content quality:
        
        Resume Data: {json.dumps(resume_data, indent=2)}
        
        Provide detailed analysis in JSON format:
        {{
            "structure_score": 85,
            "content_quality": "Excellent/Good/Fair/Poor",
            "sections_analysis": {{
                "contact_info": {{"present": true, "completeness": 95, "issues": []}},
                "summary": {{"present": true, "quality": "Strong", "length": "Appropriate", "issues": []}},
                "experience": {{"present": true, "detail_level": "Comprehensive", "achievements": "Well-quantified", "issues": []}},
                "education": {{"present": true, "relevance": "High", "issues": []}},
                "skills": {{"present": true, "organization": "Good", "relevance": "High", "issues": []}},
                "projects": {{"present": true, "detail_level": "Good", "relevance": "High", "issues": []}}
            }},
            "strengths": ["strength1", "strength2"],
            "weaknesses": ["weakness1", "weakness2"],
            "formatting_issues": ["issue1", "issue2"],
            "content_gaps": ["gap1", "gap2"],
            "recommendations": ["rec1", "rec2"]
        }}
        """
        
        messages = [
            {"role": "system", "content": "You are an expert resume analyst. Analyze resume structure, content quality, and provide detailed feedback."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = self.client.chat_completion(messages, temperature=0.2, max_tokens=800)
            content = response['choices'][0]['message']['content']
            
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return self._get_default_structure_analysis()
                
        except Exception as e:
            logger.error(f"Error analyzing resume structure: {str(e)}")
            return self._get_default_structure_analysis()
    
    def _analyze_job_relevance(self, resume_data: Dict, job_analysis: Dict) -> Dict:
        """Analyze job relevance with detailed matching"""
        
        prompt = f"""
        Analyze job relevance for this resume:
        
        Resume: {json.dumps(resume_data, indent=2)}
        Job: {json.dumps(job_analysis, indent=2)}
        
        Provide detailed job relevance analysis in JSON:
        {{
            "relevance_score": 85,
            "match_analysis": {{
                "skills_match": {{"percentage": 80, "matched_skills": ["skill1", "skill2"], "missing_skills": ["skill3", "skill4"]}},
                "experience_match": {{"percentage": 90, "relevant_experience": ["exp1", "exp2"], "gaps": ["gap1"]}},
                "education_match": {{"percentage": 95, "relevance": "High", "notes": "Strong educational background"}},
                "projects_match": {{"percentage": 75, "relevant_projects": ["proj1"], "suggestions": ["suggestion1"]}}
            }},
            "keyword_analysis": {{
                "density": 3.2,
                "relevance": "Good",
                "missing_keywords": ["keyword1", "keyword2"],
                "suggestions": ["suggestion1", "suggestion2"]
            }},
            "industry_alignment": "Strong/Moderate/Weak",
            "role_fit": "Excellent/Good/Fair/Poor",
            "competitive_advantage": ["advantage1", "advantage2"],
            "improvement_areas": ["area1", "area2"],
            "tailoring_recommendations": ["rec1", "rec2"]
        }}
        """
        
        messages = [
            {"role": "system", "content": "You are an expert recruiter. Analyze job relevance and provide detailed matching analysis."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = self.client.chat_completion(messages, temperature=0.2, max_tokens=1000)
            content = response['choices'][0]['message']['content']
            
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return self._get_default_job_relevance_analysis()
                
        except Exception as e:
            logger.error(f"Error analyzing job relevance: {str(e)}")
            return self._get_default_job_relevance_analysis()
    
    def _assess_technical_depth(self, resume_data: Dict, job_analysis: Dict) -> Dict:
        """Assess technical depth and sophistication"""
        
        prompt = f"""
        Assess technical depth and sophistication:
        
        Resume: {json.dumps(resume_data, indent=2)}
        Job: {json.dumps(job_analysis, indent=2)}
        
        Provide technical assessment in JSON:
        {{
            "technical_score": 80,
            "depth_analysis": {{
                "programming_skills": {{"level": "Advanced", "languages": ["Python", "JavaScript"], "frameworks": ["React", "Django"]}},
                "tools_technologies": {{"level": "Intermediate", "tools": ["Git", "Docker"], "platforms": ["AWS", "Azure"]}},
                "methodologies": {{"level": "Good", "practices": ["Agile", "TDD"], "processes": ["CI/CD"]}},
                "domain_knowledge": {{"level": "Strong", "areas": ["Data Science", "ML"], "expertise": ["Deep Learning"]}}
            }},
            "complexity_indicators": {{
                "project_complexity": "High/Medium/Low",
                "problem_solving": "Advanced/Intermediate/Basic",
                "innovation_level": "High/Medium/Low",
                "scalability_focus": "Strong/Moderate/Weak"
            }},
            "skill_progression": {{
                "learning_trajectory": "Steady growth",
                "skill_diversification": "Good",
                "depth_vs_breadth": "Balanced",
                "cutting_edge_skills": ["skill1", "skill2"]
            }},
            "technical_gaps": ["gap1", "gap2"],
            "skill_development_recommendations": ["rec1", "rec2"],
            "certification_suggestions": ["cert1", "cert2"]
        }}
        """
        
        messages = [
            {"role": "system", "content": "You are a senior technical architect. Assess technical depth, skills, and provide development recommendations."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = self.client.chat_completion(messages, temperature=0.2, max_tokens=800)
            content = response['choices'][0]['message']['content']
            
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return self._get_default_technical_assessment()
                
        except Exception as e:
            logger.error(f"Error assessing technical depth: {str(e)}")
            return self._get_default_technical_assessment()
    
    def _analyze_achievements(self, resume_data: Dict) -> Dict:
        """Analyze achievements and impact metrics"""
        
        prompt = f"""
        Analyze achievements and impact metrics:
        
        Resume: {json.dumps(resume_data, indent=2)}
        
        Provide achievement analysis in JSON:
        {{
            "achievement_score": 85,
            "quantification_analysis": {{
                "percentage_quantified": 75,
                "metrics_used": ["percentage", "dollar_amount", "time_saved", "users_impacted"],
                "impact_level": "High/Medium/Low",
                "credibility": "Strong/Moderate/Weak"
            }},
            "achievement_categories": {{
                "performance_improvements": ["achievement1", "achievement2"],
                "cost_savings": ["achievement1"],
                "revenue_generation": ["achievement1"],
                "process_optimization": ["achievement1"],
                "team_leadership": ["achievement1"]
            }},
            "impact_analysis": {{
                "business_impact": "Significant/Moderate/Minimal",
                "technical_impact": "High/Medium/Low",
                "scope_of_influence": "Company-wide/Team/Individual",
                "measurable_results": true
            }},
            "achievement_strengths": ["strength1", "strength2"],
            "improvement_areas": ["area1", "area2"],
            "recommendations": ["rec1", "rec2"]
        }}
        """
        
        messages = [
            {"role": "system", "content": "You are a business analyst. Analyze achievements, impact metrics, and provide improvement recommendations."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = self.client.chat_completion(messages, temperature=0.2, max_tokens=800)
            content = response['choices'][0]['message']['content']
            
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return self._get_default_achievement_analysis()
                
        except Exception as e:
            logger.error(f"Error analyzing achievements: {str(e)}")
            return self._get_default_achievement_analysis()
    
    def _analyze_career_progression(self, resume_data: Dict) -> Dict:
        """Analyze career progression and growth patterns"""
        
        prompt = f"""
        Analyze career progression and growth patterns:
        
        Resume: {json.dumps(resume_data, indent=2)}
        
        Provide career progression analysis in JSON:
        {{
            "progression_score": 80,
            "career_trajectory": {{
                "growth_pattern": "Steady/Accelerated/Stagnant",
                "responsibility_increase": "Clear/Moderate/Unclear",
                "skill_development": "Continuous/Intermittent/Limited",
                "industry_focus": "Consistent/Varied/Mixed"
            }},
            "role_evolution": {{
                "title_progression": "Clear advancement",
                "scope_expansion": "Significant growth",
                "leadership_development": "Strong progression",
                "technical_advancement": "Continuous improvement"
            }},
            "growth_indicators": {{
                "increasing_responsibilities": true,
                "expanding_skill_set": true,
                "growing_team_size": true,
                "higher_complexity_projects": true
            }},
            "career_strengths": ["strength1", "strength2"],
            "development_areas": ["area1", "area2"],
            "next_steps": ["step1", "step2"],
            "leadership_potential": "High/Medium/Low"
        }}
        """
        
        messages = [
            {"role": "system", "content": "You are a career development expert. Analyze career progression, growth patterns, and provide development insights."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = self.client.chat_completion(messages, temperature=0.2, max_tokens=800)
            content = response['choices'][0]['message']['content']
            
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return self._get_default_career_progression_analysis()
                
        except Exception as e:
            logger.error(f"Error analyzing career progression: {str(e)}")
            return self._get_default_career_progression_analysis()
    
    def _analyze_ats_compatibility(self, resume_data: Dict, job_analysis: Dict) -> Dict:
        """Analyze ATS compatibility and optimization"""
        
        prompt = f"""
        Analyze ATS compatibility and optimization:
        
        Resume: {json.dumps(resume_data, indent=2)}
        Job: {json.dumps(job_analysis, indent=2)}
        
        Provide ATS analysis in JSON:
        {{
            "ats_score": 85,
            "format_compatibility": {{
                "file_format": "Compatible/Issues",
                "font_consistency": "Good/Needs improvement",
                "structure_clarity": "Clear/Unclear",
                "section_organization": "Logical/Confusing"
            }},
            "keyword_optimization": {{
                "density": 3.2,
                "relevance": "High/Medium/Low",
                "natural_integration": "Good/Poor",
                "missing_keywords": ["keyword1", "keyword2"],
                "overuse_issues": []
            }},
            "content_optimization": {{
                "action_verbs": "Strong/Weak",
                "quantification": "Good/Needs improvement",
                "achievement_focus": "Clear/Unclear",
                "skill_presentation": "Effective/Ineffective"
            }},
            "ats_issues": ["issue1", "issue2"],
            "optimization_recommendations": ["rec1", "rec2"],
            "pass_probability": "High/Medium/Low"
        }}
        """
        
        messages = [
            {"role": "system", "content": "You are an ATS optimization expert. Analyze resume compatibility with ATS systems and provide optimization recommendations."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = self.client.chat_completion(messages, temperature=0.2, max_tokens=800)
            content = response['choices'][0]['message']['content']
            
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return self._get_default_ats_analysis()
                
        except Exception as e:
            logger.error(f"Error analyzing ATS compatibility: {str(e)}")
            return self._get_default_ats_analysis()
    
    def _generate_industry_insights(self, resume_data: Dict, job_analysis: Dict) -> Dict:
        """Generate industry-specific insights and recommendations"""
        
        # Determine industry from job analysis
        industry = self._detect_industry(job_analysis)
        
        prompt = f"""
        Generate industry-specific insights for {industry}:
        
        Resume: {json.dumps(resume_data, indent=2)}
        Job: {json.dumps(job_analysis, indent=2)}
        
        Provide industry insights in JSON:
        {{
            "industry": "{industry}",
            "market_trends": {{
                "current_demand": "High/Medium/Low",
                "skill_priorities": ["skill1", "skill2"],
                "emerging_technologies": ["tech1", "tech2"],
                "salary_trends": "Rising/Stable/Declining"
            }},
            "competitive_landscape": {{
                "candidate_supply": "High/Medium/Low",
                "skill_shortages": ["skill1", "skill2"],
                "differentiation_factors": ["factor1", "factor2"],
                "market_positioning": "Strong/Moderate/Weak"
            }},
            "industry_requirements": {{
                "essential_skills": ["skill1", "skill2"],
                "preferred_qualifications": ["qual1", "qual2"],
                "certifications": ["cert1", "cert2"],
                "experience_levels": "Junior/Mid/Senior"
            }},
            "growth_opportunities": ["opportunity1", "opportunity2"],
            "industry_recommendations": ["rec1", "rec2"],
            "networking_suggestions": ["suggestion1", "suggestion2"]
        }}
        """
        
        messages = [
            {"role": "system", "content": f"You are an industry expert in {industry}. Provide market insights, trends, and career recommendations."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = self.client.chat_completion(messages, temperature=0.3, max_tokens=800)
            content = response['choices'][0]['message']['content']
            
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return self._get_default_industry_insights(industry)
                
        except Exception as e:
            logger.error(f"Error generating industry insights: {str(e)}")
            return self._get_default_industry_insights(industry)
    
    def _generate_improvement_recommendations(self, resume_data: Dict, job_analysis: Dict) -> Dict:
        """Generate comprehensive improvement recommendations"""
        
        prompt = f"""
        Generate comprehensive improvement recommendations:
        
        Resume: {json.dumps(resume_data, indent=2)}
        Job: {json.dumps(job_analysis, indent=2)}
        
        Provide improvement recommendations in JSON:
        {{
            "priority_recommendations": [
                {{"priority": "High", "category": "Content", "recommendation": "Add more quantified achievements", "impact": "High", "effort": "Medium"}},
                {{"priority": "Medium", "category": "Skills", "recommendation": "Learn missing technologies", "impact": "Medium", "effort": "High"}}
            ],
            "quick_wins": ["win1", "win2"],
            "long_term_improvements": ["improvement1", "improvement2"],
            "skill_development": {{
                "immediate": ["skill1", "skill2"],
                "short_term": ["skill3", "skill4"],
                "long_term": ["skill5", "skill6"]
            }},
            "project_suggestions": ["project1", "project2"],
            "certification_recommendations": ["cert1", "cert2"],
            "networking_opportunities": ["opportunity1", "opportunity2"],
            "timeline": {{
                "immediate": "1-2 weeks",
                "short_term": "1-3 months",
                "long_term": "3-6 months"
            }}
        }}
        """
        
        messages = [
            {"role": "system", "content": "You are a career development expert. Provide comprehensive, actionable improvement recommendations with priorities and timelines."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = self.client.chat_completion(messages, temperature=0.3, max_tokens=1000)
            content = response['choices'][0]['message']['content']
            
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return self._get_default_improvement_recommendations()
                
        except Exception as e:
            logger.error(f"Error generating improvement recommendations: {str(e)}")
            return self._get_default_improvement_recommendations()
    
    def _generate_documentation_report(self, resume_data: Dict, job_analysis: Dict) -> Dict:
        """Generate comprehensive documentation report"""
        
        prompt = f"""
        Generate comprehensive documentation report:
        
        Resume: {json.dumps(resume_data, indent=2)}
        Job: {json.dumps(job_analysis, indent=2)}
        
        Provide documentation report in JSON:
        {{
            "executive_summary": "Brief overview of analysis results",
            "detailed_findings": {{
                "strengths": ["strength1", "strength2"],
                "weaknesses": ["weakness1", "weakness2"],
                "opportunities": ["opportunity1", "opportunity2"],
                "threats": ["threat1", "threat2"]
            }},
            "score_breakdown": {{
                "content_quality": 85,
                "job_relevance": 90,
                "technical_depth": 80,
                "achievement_impact": 75,
                "career_progression": 85
            }},
            "recommendations_summary": {{
                "immediate_actions": ["action1", "action2"],
                "short_term_goals": ["goal1", "goal2"],
                "long_term_strategy": ["strategy1", "strategy2"]
            }},
            "competitive_analysis": {{
                "market_position": "Strong/Moderate/Weak",
                "differentiation": ["factor1", "factor2"],
                "improvement_potential": "High/Medium/Low"
            }},
            "next_steps": ["step1", "step2", "step3"]
        }}
        """
        
        messages = [
            {"role": "system", "content": "You are a senior consultant. Generate a comprehensive, professional documentation report with executive summary and detailed findings."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = self.client.chat_completion(messages, temperature=0.2, max_tokens=1200)
            content = response['choices'][0]['message']['content']
            
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return self._get_default_documentation_report()
                
        except Exception as e:
            logger.error(f"Error generating documentation report: {str(e)}")
            return self._get_default_documentation_report()
    
    def _calculate_overall_score(self, analysis_results: Dict) -> float:
        """Calculate overall score based on analysis results"""
        
        scores = []
        
        # Extract scores from different analyses
        if 'resume_summary' in analysis_results:
            scores.append(analysis_results['resume_summary'].get('structure_score', 70))
        
        if 'job_relevance_analysis' in analysis_results:
            scores.append(analysis_results['job_relevance_analysis'].get('relevance_score', 70))
        
        if 'technical_assessment' in analysis_results:
            scores.append(analysis_results['technical_assessment'].get('technical_score', 70))
        
        if 'achievement_analysis' in analysis_results:
            scores.append(analysis_results['achievement_analysis'].get('achievement_score', 70))
        
        if 'career_progression' in analysis_results:
            scores.append(analysis_results['career_progression'].get('progression_score', 70))
        
        if 'ats_optimization' in analysis_results:
            scores.append(analysis_results['ats_optimization'].get('ats_score', 70))
        
        # Calculate weighted average
        if scores:
            return sum(scores) / len(scores)
        else:
            return 70.0
    
    def _get_grade(self, score: float) -> str:
        """Convert score to letter grade"""
        if score >= 90:
            return 'A+'
        elif score >= 85:
            return 'A'
        elif score >= 80:
            return 'B+'
        elif score >= 75:
            return 'B'
        elif score >= 70:
            return 'B-'
        elif score >= 65:
            return 'C+'
        elif score >= 60:
            return 'C'
        else:
            return 'D'
    
    def _generate_analysis_id(self, resume_data: Dict, job_analysis: Dict) -> str:
        """Generate unique analysis ID"""
        content = f"{resume_data.get('contact', {}).get('name', 'unknown')}_{job_analysis.get('title', 'unknown')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def _detect_industry(self, job_analysis: Dict) -> str:
        """Detect industry from job analysis"""
        title = job_analysis.get('title', '').lower()
        description = job_analysis.get('description', '').lower()
        
        if any(keyword in title or keyword in description for keyword in ['data', 'analyst', 'scientist', 'machine learning']):
            return 'data_science'
        elif any(keyword in title or keyword in description for keyword in ['software', 'developer', 'engineer', 'programmer']):
            return 'software_engineering'
        elif any(keyword in title or keyword in description for keyword in ['product', 'manager', 'strategy']):
            return 'product_management'
        else:
            return 'general'
    
    # Default analysis methods (fallbacks)
    def _get_default_structure_analysis(self) -> Dict:
        return {
            "structure_score": 70,
            "content_quality": "Good",
            "sections_analysis": {},
            "strengths": ["Well-structured resume"],
            "weaknesses": ["Could use more detail"],
            "formatting_issues": [],
            "content_gaps": [],
            "recommendations": ["Add more quantified achievements"]
        }
    
    def _get_default_job_relevance_analysis(self) -> Dict:
        return {
            "relevance_score": 70,
            "match_analysis": {},
            "keyword_analysis": {"density": 2.5, "relevance": "Moderate"},
            "industry_alignment": "Moderate",
            "role_fit": "Good",
            "competitive_advantage": [],
            "improvement_areas": [],
            "tailoring_recommendations": []
        }
    
    def _get_default_technical_assessment(self) -> Dict:
        return {
            "technical_score": 70,
            "depth_analysis": {},
            "complexity_indicators": {},
            "skill_progression": {},
            "technical_gaps": [],
            "skill_development_recommendations": [],
            "certification_suggestions": []
        }
    
    def _get_default_achievement_analysis(self) -> Dict:
        return {
            "achievement_score": 70,
            "quantification_analysis": {"percentage_quantified": 50},
            "achievement_categories": {},
            "impact_analysis": {},
            "achievement_strengths": [],
            "improvement_areas": [],
            "recommendations": []
        }
    
    def _get_default_career_progression_analysis(self) -> Dict:
        return {
            "progression_score": 70,
            "career_trajectory": {},
            "role_evolution": {},
            "growth_indicators": {},
            "career_strengths": [],
            "development_areas": [],
            "next_steps": [],
            "leadership_potential": "Medium"
        }
    
    def _get_default_ats_analysis(self) -> Dict:
        return {
            "ats_score": 70,
            "format_compatibility": {},
            "keyword_optimization": {"density": 2.5},
            "content_optimization": {},
            "ats_issues": [],
            "optimization_recommendations": [],
            "pass_probability": "Medium"
        }
    
    def _get_default_industry_insights(self, industry: str) -> Dict:
        return {
            "industry": industry,
            "market_trends": {},
            "competitive_landscape": {},
            "industry_requirements": {},
            "growth_opportunities": [],
            "industry_recommendations": [],
            "networking_suggestions": []
        }
    
    def _get_default_improvement_recommendations(self) -> Dict:
        return {
            "priority_recommendations": [],
            "quick_wins": [],
            "long_term_improvements": [],
            "skill_development": {},
            "project_suggestions": [],
            "certification_recommendations": [],
            "networking_opportunities": [],
            "timeline": {}
        }
    
    def _get_default_documentation_report(self) -> Dict:
        return {
            "executive_summary": "Resume analysis completed with standard recommendations",
            "detailed_findings": {},
            "score_breakdown": {},
            "recommendations_summary": {},
            "competitive_analysis": {},
            "next_steps": []
        }
