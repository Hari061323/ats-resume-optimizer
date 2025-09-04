"""
AI Keyword Analyzer
Extracts keywords from job descriptions and matches with resume
"""

import json
import re
import os
from typing import Dict, List, Set, Tuple, Any
from collections import Counter
import requests
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
# Look for .env in parent directory (project root)
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


class AIKeywordAnalyzer:
    """Analyze keywords using AI for semantic matching"""
    
    def __init__(self):
        self.client = OpenAIClient()
        
        # Common ATS keywords by category
        self.keyword_categories = {
            'action_verbs': [
                'achieved', 'accelerated', 'accomplished', 'administered', 'analyzed',
                'built', 'collaborated', 'created', 'delivered', 'designed', 'developed',
                'drove', 'enhanced', 'established', 'executed', 'generated', 'implemented',
                'improved', 'increased', 'launched', 'led', 'managed', 'optimized',
                'orchestrated', 'pioneered', 'reduced', 'resolved', 'spearheaded',
                'streamlined', 'transformed', 'upgraded'
            ],
            'metrics': [
                'ROI', 'KPI', 'revenue', 'cost reduction', 'efficiency', 'performance',
                'growth', 'optimization', 'productivity', 'quality', 'satisfaction',
                'retention', 'acquisition', 'conversion', 'engagement'
            ]
        }
    
    def extract_keywords_from_job(self, job_description: str) -> Dict[str, Any]:
        """Extract keywords from job description using AI"""
        
        prompt = """Analyze this job description and extract:
        1. Required Skills (technical and soft skills)
        2. Tools and Technologies
        3. Responsibilities (key action words)
        4. Qualifications (degrees, certifications, years of experience)
        5. Industry Keywords (domain-specific terms)
        6. Nice-to-have Skills
        
        Return as JSON:
        {
            "required_skills": [],
            "tools_technologies": [],
            "responsibilities": [],
            "qualifications": [],
            "industry_keywords": [],
            "nice_to_have": [],
            "experience_years": 0,
            "education_level": "",
            "job_level": ""
        }"""
        
        messages = [
            {"role": "system", "content": "You are an expert ATS keyword analyzer. Extract all important keywords that an ATS system would look for."},
            {"role": "user", "content": f"{prompt}\n\nJob Description:\n{job_description}"}
        ]
        
        try:
            response = self.client.chat_completion(messages, temperature=0.3)
            content = response['choices'][0]['message']['content']
            
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                keywords = json.loads(json_match.group())
            else:
                keywords = json.loads(content)
            
            # Add frequency analysis
            keywords['keyword_frequency'] = self._analyze_frequency(job_description)
            
            return keywords
            
        except Exception as e:
            logger.error(f"Error extracting keywords: {str(e)}")
            return self._extract_keywords_fallback(job_description)
    
    def _extract_keywords_fallback(self, text: str) -> Dict[str, Any]:
        """Fallback keyword extraction without AI"""
        words = text.lower().split()
        
        # Common technical skills
        tech_skills = ['python', 'java', 'javascript', 'sql', 'aws', 'docker', 
                      'kubernetes', 'react', 'angular', 'node', 'git', 'agile',
                      'machine learning', 'data science', 'devops', 'cloud']
        
        found_skills = [skill for skill in tech_skills if skill in text.lower()]
        
        return {
            "required_skills": found_skills,
            "tools_technologies": [],
            "responsibilities": [],
            "qualifications": [],
            "industry_keywords": [],
            "nice_to_have": [],
            "experience_years": self._extract_years(text),
            "education_level": self._extract_education_level(text),
            "job_level": self._extract_job_level(text),
            "keyword_frequency": self._analyze_frequency(text)
        }
    
    def _analyze_frequency(self, text: str) -> Dict[str, int]:
        """Analyze keyword frequency in text"""
        # Clean text
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        words = text.split()
        
        # Filter stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                     'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were'}
        words = [w for w in words if w not in stop_words and len(w) > 2]
        
        # Count frequency
        return dict(Counter(words).most_common(30))
    
    def _extract_years(self, text: str) -> int:
        """Extract years of experience from text"""
        patterns = [
            r'(\d+)\+?\s*years?\s*(?:of\s*)?experience',
            r'(\d+)\+?\s*years?\s*(?:of\s*)?professional',
            r'minimum\s*(?:of\s*)?(\d+)\s*years?'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                return int(match.group(1))
        return 0
    
    def _extract_education_level(self, text: str) -> str:
        """Extract education level from text"""
        education_levels = {
            'phd': 'PhD',
            'doctorate': 'PhD',
            'master': 'Master',
            'mba': 'MBA',
            'bachelor': 'Bachelor',
            'associate': 'Associate'
        }
        
        text_lower = text.lower()
        for key, value in education_levels.items():
            if key in text_lower:
                return value
        return 'Bachelor'  # Default
    
    def _extract_job_level(self, text: str) -> str:
        """Extract job level from text"""
        levels = {
            'senior': 'Senior',
            'lead': 'Lead',
            'principal': 'Principal',
            'staff': 'Staff',
            'junior': 'Junior',
            'entry': 'Entry'
        }
        
        text_lower = text.lower()
        for key, value in levels.items():
            if key in text_lower:
                return value
        return 'Mid-Level'  # Default
    
    def match_keywords(self, resume_text: str, job_keywords: Dict) -> Dict[str, Any]:
        """Match resume keywords with job keywords"""
        
        resume_lower = resume_text.lower()
        
        # Extract all keyword lists from job
        all_job_keywords = set()
        for key in ['required_skills', 'tools_technologies', 'responsibilities', 
                   'qualifications', 'industry_keywords']:
            if key in job_keywords:
                all_job_keywords.update([kw.lower() for kw in job_keywords[key]])
        
        # Find exact matches
        exact_matches = []
        for keyword in all_job_keywords:
            if keyword in resume_lower:
                exact_matches.append(keyword)
        
        # Find semantic matches using AI
        semantic_matches = self._find_semantic_matches(resume_text, list(all_job_keywords))
        
        # Find missing keywords
        matched_keywords = set(exact_matches) | set(semantic_matches)
        missing_keywords = list(all_job_keywords - matched_keywords)
        
        # Calculate match percentage
        total_keywords = len(all_job_keywords) if all_job_keywords else 1
        match_percentage = (len(matched_keywords) / total_keywords) * 100
        
        return {
            'exact_matches': exact_matches,
            'semantic_matches': semantic_matches,
            'missing_keywords': missing_keywords[:20],  # Top 20 missing
            'match_percentage': round(match_percentage, 2),
            'total_keywords': total_keywords,
            'matched_count': len(matched_keywords),
            'keyword_density': self._calculate_keyword_density(resume_text, matched_keywords),
            'recommendations': self._generate_recommendations(missing_keywords, job_keywords)
        }
    
    def _find_semantic_matches(self, resume_text: str, job_keywords: List[str]) -> List[str]:
        """Find semantically similar keywords using AI"""
        
        if not job_keywords:
            return []
        
        prompt = f"""Given this resume text, identify which of these job keywords are semantically present 
        (even if not exact matches). For example, 'team leadership' matches 'led team'.
        
        Job Keywords: {', '.join(job_keywords[:30])}
        
        Return only the job keywords that have semantic matches in the resume as a JSON array."""
        
        messages = [
            {"role": "system", "content": "You are an expert at identifying semantic keyword matches."},
            {"role": "user", "content": f"{prompt}\n\nResume:\n{resume_text[:3000]}"}
        ]
        
        try:
            response = self.client.chat_completion(messages, temperature=0.3, max_tokens=500)
            content = response['choices'][0]['message']['content']
            
            # Extract JSON array
            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            return []
            
        except Exception as e:
            logger.error(f"Error in semantic matching: {str(e)}")
            return []
    
    def _calculate_keyword_density(self, text: str, keywords: Set[str]) -> float:
        """Calculate keyword density in text"""
        total_words = len(text.split())
        keyword_count = sum(text.lower().count(kw.lower()) for kw in keywords)
        
        if total_words == 0:
            return 0.0
        
        density = (keyword_count / total_words) * 100
        return round(min(density, 10.0), 2)  # Cap at 10% to avoid keyword stuffing
    
    def _generate_recommendations(self, missing_keywords: List[str], 
                                 job_keywords: Dict) -> List[Dict[str, str]]:
        """Generate recommendations for adding missing keywords"""
        
        recommendations = []
        
        # Group missing keywords by category
        skill_keywords = [kw for kw in missing_keywords 
                         if kw in job_keywords.get('required_skills', [])][:5]
        tech_keywords = [kw for kw in missing_keywords 
                        if kw in job_keywords.get('tools_technologies', [])][:5]
        
        if skill_keywords:
            recommendations.append({
                'type': 'skills',
                'keywords': skill_keywords,
                'suggestion': f"Add these skills to your skills section: {', '.join(skill_keywords)}"
            })
        
        if tech_keywords:
            recommendations.append({
                'type': 'technologies',
                'keywords': tech_keywords,
                'suggestion': f"Mention experience with: {', '.join(tech_keywords)}"
            })
        
        # Action verb recommendations
        if missing_keywords:
            action_verbs = [kw for kw in missing_keywords 
                           if kw in self.keyword_categories['action_verbs']][:3]
            if action_verbs:
                recommendations.append({
                    'type': 'action_verbs',
                    'keywords': action_verbs,
                    'suggestion': f"Use stronger action verbs like: {', '.join(action_verbs)}"
                })
        
        return recommendations
    
    def get_industry_keywords(self, industry: str) -> List[str]:
        """Get industry-specific keywords"""
        
        industry_keywords = {
            'technology': ['agile', 'scrum', 'ci/cd', 'cloud', 'api', 'microservices',
                          'scalability', 'optimization', 'automation', 'devops'],
            'finance': ['risk management', 'compliance', 'portfolio', 'trading',
                       'analysis', 'forecasting', 'regulatory', 'audit'],
            'healthcare': ['patient care', 'hipaa', 'clinical', 'diagnosis',
                          'treatment', 'medical records', 'healthcare systems'],
            'marketing': ['seo', 'sem', 'roi', 'conversion', 'engagement',
                         'campaign', 'analytics', 'brand', 'content strategy'],
            'sales': ['quota', 'pipeline', 'crm', 'lead generation', 'closing',
                     'negotiation', 'relationship building', 'revenue growth']
        }
        
        return industry_keywords.get(industry.lower(), [])