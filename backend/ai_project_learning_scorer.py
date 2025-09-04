"""
AI Project Learning-Based Scorer
Advanced AI system that learns from project patterns and evaluates job relevance
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

class AIProjectLearningScorer:
    """
    Advanced AI system that learns from project patterns and evaluates:
    1. Project complexity and depth
    2. Technology stack relevance
    3. Problem-solving approach
    4. Learning progression
    5. Job-specific project alignment
    """
    
    def __init__(self):
        self.client = OpenAIClient()
        
        # Learning-based scoring weights
        self.weights = {
            'project_relevance': 0.30,      # 30% - How relevant projects are to job
            'technical_depth': 0.25,        # 25% - Complexity and technical sophistication
            'learning_progression': 0.20,   # 20% - Shows growth and learning
            'problem_solving': 0.15,        # 15% - Problem-solving approach
            'impact_metrics': 0.10          # 10% - Measurable impact and results
        }
        
        # Project complexity levels
        self.complexity_levels = {
            'beginner': {'score': 30, 'keywords': ['basic', 'simple', 'tutorial', 'learning']},
            'intermediate': {'score': 60, 'keywords': ['application', 'system', 'integration']},
            'advanced': {'score': 85, 'keywords': ['architecture', 'scalable', 'enterprise', 'optimization']},
            'expert': {'score': 100, 'keywords': ['machine learning', 'ai', 'distributed', 'microservices']}
        }
        
        # Technology relevance patterns
        self.tech_patterns = {
            'data_science': ['python', 'r', 'sql', 'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch'],
            'web_development': ['javascript', 'react', 'node.js', 'python', 'django', 'flask', 'html', 'css'],
            'mobile_development': ['swift', 'kotlin', 'react native', 'flutter', 'android', 'ios'],
            'cloud_devops': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'jenkins'],
            'backend_development': ['python', 'java', 'c#', 'node.js', 'spring', 'django', 'fastapi'],
            'frontend_development': ['react', 'vue', 'angular', 'javascript', 'typescript', 'html', 'css']
        }
    
    def calculate_project_score(self, resume_data: Dict, job_analysis: Dict) -> Dict[str, Any]:
        """
        Calculate comprehensive project-based score using AI learning
        """
        projects = resume_data.get('projects', [])
        job_description = job_analysis.get('description', '')
        job_title = job_analysis.get('title', '')
        
        if not projects:
            return self._get_no_projects_score()
        
        # AI-powered project analysis
        project_analysis = self._analyze_projects_with_ai(projects, job_description, job_title)
        
        # Calculate individual component scores
        scores = {
            'project_relevance': self._score_project_relevance(projects, job_analysis, project_analysis),
            'technical_depth': self._score_technical_depth(projects, project_analysis),
            'learning_progression': self._score_learning_progression(projects, project_analysis),
            'problem_solving': self._score_problem_solving(projects, project_analysis),
            'impact_metrics': self._score_impact_metrics(projects, project_analysis)
        }
        
        # Calculate weighted total
        total_score = sum(scores[key] * self.weights[key] for key in scores)
        
        # Generate detailed insights
        insights = self._generate_project_insights(projects, job_analysis, scores, project_analysis)
        
        # Learning recommendations
        recommendations = self._generate_learning_recommendations(projects, job_analysis, scores)
        
        return {
            'total_score': round(total_score, 2),
            'component_scores': scores,
            'weighted_scores': {k: round(v * self.weights[k], 2) for k, v in scores.items()},
            'project_analysis': project_analysis,
            'insights': insights,
            'recommendations': recommendations,
            'learning_path': self._suggest_learning_path(projects, job_analysis),
            'timestamp': datetime.now().isoformat()
        }
    
    def _analyze_projects_with_ai(self, projects: List[Dict], job_description: str, job_title: str) -> Dict:
        """Use AI to analyze project patterns and learning progression"""
        
        prompt = f"""
        Analyze these projects for a {job_title} position:
        
        Job Description: {job_description[:500]}...
        
        Projects: {json.dumps(projects, indent=2)}
        
        For each project, analyze:
        1. Technical complexity level (beginner/intermediate/advanced/expert)
        2. Technology stack relevance to the job
        3. Problem-solving approach and methodology
        4. Learning progression indicators
        5. Impact and measurable results
        6. Innovation and creativity level
        
        Return analysis as JSON with this structure:
        {{
            "projects": [
                {{
                    "name": "project_name",
                    "complexity_level": "advanced",
                    "relevance_score": 85,
                    "technologies_used": ["tech1", "tech2"],
                    "problem_solving_approach": "description",
                    "learning_indicators": ["indicator1", "indicator2"],
                    "impact_metrics": ["metric1", "metric2"],
                    "innovation_level": "high/medium/low",
                    "job_alignment": "strong/moderate/weak"
                }}
            ],
            "overall_analysis": {{
                "learning_progression": "description",
                "technical_growth": "description",
                "strengths": ["strength1", "strength2"],
                "areas_for_improvement": ["area1", "area2"],
                "career_trajectory": "description"
            }}
        }}
        """
        
        messages = [
            {"role": "system", "content": "You are an expert technical recruiter and career advisor. Analyze projects for learning patterns, technical depth, and job relevance."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = self.client.chat_completion(messages, temperature=0.3, max_tokens=1500)
            content = response['choices'][0]['message']['content']
            
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return self._get_default_project_analysis(projects)
                
        except Exception as e:
            logger.error(f"Error analyzing projects with AI: {str(e)}")
            return self._get_default_project_analysis(projects)
    
    def _score_project_relevance(self, projects: List[Dict], job_analysis: Dict, project_analysis: Dict) -> float:
        """Score how relevant projects are to the target job"""
        if not projects:
            return 0
        
        total_relevance = 0
        for i, project in enumerate(projects):
            if i < len(project_analysis.get('projects', [])):
                relevance_score = project_analysis['projects'][i].get('relevance_score', 50)
                total_relevance += relevance_score
            else:
                # Fallback scoring
                total_relevance += self._calculate_basic_relevance(project, job_analysis)
        
        return min(total_relevance / len(projects), 100)
    
    def _score_technical_depth(self, projects: List[Dict], project_analysis: Dict) -> float:
        """Score technical complexity and depth of projects"""
        if not projects:
            return 0
        
        total_depth = 0
        for i, project in enumerate(projects):
            if i < len(project_analysis.get('projects', [])):
                complexity = project_analysis['projects'][i].get('complexity_level', 'intermediate')
                depth_score = self.complexity_levels.get(complexity, {'score': 60})['score']
                total_depth += depth_score
            else:
                # Fallback scoring based on project description
                total_depth += self._estimate_complexity(project)
        
        return min(total_depth / len(projects), 100)
    
    def _score_learning_progression(self, projects: List[Dict], project_analysis: Dict) -> float:
        """Score learning progression and growth patterns"""
        if len(projects) < 2:
            return 50  # Can't assess progression with single project
        
        # Analyze progression using AI insights
        overall_analysis = project_analysis.get('overall_analysis', {})
        learning_progression = overall_analysis.get('learning_progression', '')
        
        # Score based on progression indicators
        progression_score = 50  # Base score
        
        if 'advanced' in learning_progression.lower() or 'growth' in learning_progression.lower():
            progression_score += 30
        if 'complex' in learning_progression.lower() or 'sophisticated' in learning_progression.lower():
            progression_score += 20
        if 'innovation' in learning_progression.lower() or 'creative' in learning_progression.lower():
            progression_score += 15
        
        return min(progression_score, 100)
    
    def _score_problem_solving(self, projects: List[Dict], project_analysis: Dict) -> float:
        """Score problem-solving approach and methodology"""
        if not projects:
            return 0
        
        total_approach = 0
        for i, project in enumerate(projects):
            if i < len(project_analysis.get('projects', [])):
                approach = project_analysis['projects'][i].get('problem_solving_approach', '')
                # Score based on approach quality
                approach_score = 50
                if 'systematic' in approach.lower() or 'methodical' in approach.lower():
                    approach_score += 20
                if 'innovative' in approach.lower() or 'creative' in approach.lower():
                    approach_score += 15
                if 'optimization' in approach.lower() or 'efficiency' in approach.lower():
                    approach_score += 15
                total_approach += min(approach_score, 100)
            else:
                total_approach += 50  # Default score
        
        return min(total_approach / len(projects), 100)
    
    def _score_impact_metrics(self, projects: List[Dict], project_analysis: Dict) -> float:
        """Score measurable impact and results"""
        if not projects:
            return 0
        
        total_impact = 0
        for i, project in enumerate(projects):
            if i < len(project_analysis.get('projects', [])):
                metrics = project_analysis['projects'][i].get('impact_metrics', [])
                # Score based on number and quality of metrics
                impact_score = len(metrics) * 15
                if any('performance' in metric.lower() or 'efficiency' in metric.lower() for metric in metrics):
                    impact_score += 20
                if any('%' in metric or 'x' in metric for metric in metrics):
                    impact_score += 15
                total_impact += min(impact_score, 100)
            else:
                # Check project description for metrics
                description = project.get('description', '')
                if any(char.isdigit() for char in description):
                    total_impact += 60  # Has some numbers
                else:
                    total_impact += 30  # No clear metrics
        
        return min(total_impact / len(projects), 100)
    
    def _generate_project_insights(self, projects: List[Dict], job_analysis: Dict, 
                                 scores: Dict, project_analysis: Dict) -> Dict:
        """Generate detailed insights about project experience"""
        
        insights = {
            'strengths': [],
            'weaknesses': [],
            'learning_patterns': [],
            'career_alignment': '',
            'technical_growth': '',
            'recommendations': []
        }
        
        # Extract insights from AI analysis
        overall_analysis = project_analysis.get('overall_analysis', {})
        
        # Strengths
        if scores['technical_depth'] >= 80:
            insights['strengths'].append('Demonstrates advanced technical skills and complex project experience')
        if scores['learning_progression'] >= 80:
            insights['strengths'].append('Shows clear learning progression and skill development')
        if scores['project_relevance'] >= 80:
            insights['strengths'].append('Projects are highly relevant to target job requirements')
        
        # Weaknesses
        if scores['impact_metrics'] < 60:
            insights['weaknesses'].append('Limited measurable impact and quantified results in projects')
        if scores['problem_solving'] < 60:
            insights['weaknesses'].append('Problem-solving approach could be more systematic')
        if len(projects) < 2:
            insights['weaknesses'].append('Limited project portfolio - consider adding more diverse projects')
        
        # Learning patterns
        insights['learning_patterns'] = overall_analysis.get('strengths', [])[:3]
        insights['career_alignment'] = overall_analysis.get('career_trajectory', '')
        insights['technical_growth'] = overall_analysis.get('technical_growth', '')
        
        return insights
    
    def _generate_learning_recommendations(self, projects: List[Dict], job_analysis: Dict, scores: Dict) -> List[str]:
        """Generate personalized learning recommendations"""
        
        recommendations = []
        
        # Based on scores
        if scores['technical_depth'] < 70:
            recommendations.append('Focus on more complex, multi-layered projects that demonstrate advanced technical skills')
        
        if scores['project_relevance'] < 70:
            job_skills = job_analysis.get('required_skills', [])
            recommendations.append(f'Develop projects using technologies relevant to the role: {", ".join(job_skills[:5])}')
        
        if scores['impact_metrics'] < 60:
            recommendations.append('Include measurable outcomes and performance metrics in project descriptions')
        
        if scores['learning_progression'] < 70:
            recommendations.append('Show clear progression from simple to complex projects over time')
        
        # General recommendations
        recommendations.extend([
            'Document your problem-solving process and methodology',
            'Include code repositories and live demos when possible',
            'Focus on projects that solve real-world problems',
            'Demonstrate both technical skills and business impact'
        ])
        
        return recommendations[:5]  # Top 5 recommendations
    
    def _suggest_learning_path(self, projects: List[Dict], job_analysis: Dict) -> Dict:
        """Suggest a personalized learning path based on current projects and job requirements"""
        
        job_skills = job_analysis.get('required_skills', [])
        current_technologies = set()
        
        # Extract current technologies from projects
        for project in projects:
            technologies = project.get('technologies', [])
            if isinstance(technologies, list):
                current_technologies.update([tech.lower() for tech in technologies])
        
        # Find gaps
        job_tech = set([skill.lower() for skill in job_skills])
        missing_skills = job_tech - current_technologies
        
        return {
            'current_technologies': list(current_technologies),
            'missing_skills': list(missing_skills)[:5],
            'next_projects': self._suggest_next_projects(missing_skills, job_analysis),
            'learning_resources': self._suggest_learning_resources(missing_skills)
        }
    
    def _suggest_next_projects(self, missing_skills: set, job_analysis: Dict) -> List[str]:
        """Suggest next projects to build based on missing skills"""
        
        suggestions = []
        job_title = job_analysis.get('title', '').lower()
        
        if 'data' in job_title or 'analyst' in job_title:
            suggestions.extend([
                'Build a machine learning model with real-world dataset',
                'Create a data visualization dashboard',
                'Develop an ETL pipeline for data processing'
            ])
        elif 'web' in job_title or 'frontend' in job_title:
            suggestions.extend([
                'Build a full-stack web application',
                'Create a responsive mobile-first website',
                'Develop a progressive web app (PWA)'
            ])
        elif 'backend' in job_title or 'api' in job_title:
            suggestions.extend([
                'Design and implement a RESTful API',
                'Build a microservices architecture',
                'Create a real-time application with WebSockets'
            ])
        else:
            suggestions.extend([
                'Build a project using the missing technologies',
                'Create a portfolio piece that demonstrates job-relevant skills',
                'Develop an open-source contribution'
            ])
        
        return suggestions[:3]
    
    def _suggest_learning_resources(self, missing_skills: set) -> List[str]:
        """Suggest learning resources for missing skills"""
        
        resources = []
        for skill in list(missing_skills)[:3]:
            if 'python' in skill:
                resources.append('Python: Complete Python Bootcamp (Udemy)')
            elif 'javascript' in skill:
                resources.append('JavaScript: The Complete Guide (Udemy)')
            elif 'react' in skill:
                resources.append('React: The Complete Course (Udemy)')
            elif 'sql' in skill:
                resources.append('SQL: Advanced Database Queries (Coursera)')
            else:
                resources.append(f'{skill.title()}: Online tutorials and documentation')
        
        return resources
    
    # Helper methods
    def _get_no_projects_score(self) -> Dict:
        """Return score for resumes with no projects"""
        return {
            'total_score': 20,
            'component_scores': {key: 20 for key in self.weights.keys()},
            'weighted_scores': {key: 20 * weight for key, weight in self.weights.items()},
            'project_analysis': {'projects': [], 'overall_analysis': {}},
            'insights': {
                'strengths': [],
                'weaknesses': ['No project portfolio - critical for technical roles'],
                'learning_patterns': [],
                'career_alignment': 'Cannot assess without project experience',
                'technical_growth': 'No project history to analyze',
                'recommendations': ['Build a portfolio of relevant projects immediately']
            },
            'recommendations': ['Start building projects relevant to your target role'],
            'learning_path': {
                'current_technologies': [],
                'missing_skills': [],
                'next_projects': ['Build your first project to demonstrate skills'],
                'learning_resources': ['Start with beginner-friendly tutorials']
            },
            'timestamp': datetime.now().isoformat()
        }
    
    def _get_default_project_analysis(self, projects: List[Dict]) -> Dict:
        """Default analysis when AI fails"""
        return {
            'projects': [
                {
                    'name': project.get('name', 'Unknown'),
                    'complexity_level': 'intermediate',
                    'relevance_score': 60,
                    'technologies_used': project.get('technologies', []),
                    'problem_solving_approach': 'Standard development approach',
                    'learning_indicators': ['Project completion'],
                    'impact_metrics': [],
                    'innovation_level': 'medium',
                    'job_alignment': 'moderate'
                }
                for project in projects
            ],
            'overall_analysis': {
                'learning_progression': 'Steady project development',
                'technical_growth': 'Consistent technical skill building',
                'strengths': ['Project completion', 'Technical implementation'],
                'areas_for_improvement': ['Documentation', 'Metrics'],
                'career_trajectory': 'Building technical foundation'
            }
        }
    
    def _calculate_basic_relevance(self, project: Dict, job_analysis: Dict) -> float:
        """Basic relevance calculation without AI"""
        job_skills = [skill.lower() for skill in job_analysis.get('required_skills', [])]
        project_tech = [tech.lower() for tech in project.get('technologies', [])]
        
        if not job_skills:
            return 60
        
        matches = len(set(job_skills) & set(project_tech))
        return min((matches / len(job_skills)) * 100, 100)
    
    def _estimate_complexity(self, project: Dict) -> float:
        """Estimate project complexity from description"""
        description = project.get('description', '').lower()
        
        for level, data in self.complexity_levels.items():
            if any(keyword in description for keyword in data['keywords']):
                return data['score']
        
        return 60  # Default intermediate
