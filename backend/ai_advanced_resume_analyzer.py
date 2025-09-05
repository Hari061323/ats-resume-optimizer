"""
Advanced AI Resume Analyzer
World-class resume analysis with cutting-edge AI techniques
"""

import os
import json
import logging
import re
import asyncio
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass
import numpy as np
from collections import Counter, defaultdict
import openai
from openai import OpenAI

logger = logging.getLogger(__name__)

@dataclass
class ResumeMetrics:
    """Comprehensive resume metrics"""
    ats_score: float
    keyword_density: float
    action_verb_usage: float
    quantifiable_achievements: float
    skills_relevance: float
    experience_alignment: float
    format_compatibility: float
    readability_score: float
    impact_score: float
    overall_score: float

@dataclass
class EnhancementSuggestion:
    """AI-generated enhancement suggestion"""
    category: str
    priority: str
    current_text: str
    suggested_text: str
    reasoning: str
    impact_score: float

class AdvancedResumeAnalyzer:
    """World-class AI resume analyzer with advanced techniques"""
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Advanced keyword banks
        self.action_verbs = {
            'leadership': ['Led', 'Directed', 'Orchestrated', 'Spearheaded', 'Championed', 'Mobilized', 'Galvanized'],
            'achievement': ['Achieved', 'Delivered', 'Exceeded', 'Surpassed', 'Accomplished', 'Secured', 'Generated'],
            'improvement': ['Optimized', 'Enhanced', 'Streamlined', 'Transformed', 'Revolutionized', 'Accelerated', 'Amplified'],
            'technical': ['Developed', 'Engineered', 'Architected', 'Implemented', 'Deployed', 'Designed', 'Built'],
            'analytical': ['Analyzed', 'Evaluated', 'Assessed', 'Investigated', 'Diagnosed', 'Researched', 'Studied'],
            'management': ['Managed', 'Supervised', 'Coordinated', 'Facilitated', 'Oversaw', 'Governed', 'Steered'],
            'innovation': ['Pioneered', 'Innovated', 'Created', 'Invented', 'Established', 'Introduced', 'Launched']
        }
        
        # ATS optimization patterns
        self.ats_patterns = {
            'contact_info': r'(?i)(email|phone|address|linkedin|github)',
            'quantified_achievements': r'\b\d+%|\$\d+|\d+\+|\d+x|\d+\.\d+',
            'action_verbs': r'\b(led|managed|developed|created|improved|increased|reduced|optimized)',
            'skills_section': r'(?i)(skills|technical skills|core competencies)',
            'experience_section': r'(?i)(experience|work history|professional experience)',
            'education_section': r'(?i)(education|academic|degree|university|college)'
        }
        
        # Industry-specific keyword weights
        self.industry_weights = {
            'technology': {
                'keywords': ['software', 'development', 'programming', 'cloud', 'AI', 'machine learning', 'data science'],
                'skills': ['Python', 'JavaScript', 'AWS', 'Docker', 'Kubernetes', 'React', 'Node.js'],
                'metrics': ['performance', 'scalability', 'efficiency', 'uptime', 'security', 'automation']
            },
            'finance': {
                'keywords': ['financial', 'analysis', 'risk', 'compliance', 'trading', 'investment', 'portfolio'],
                'skills': ['Excel', 'SQL', 'Python', 'R', 'Tableau', 'Bloomberg', 'VBA'],
                'metrics': ['ROI', 'revenue', 'cost reduction', 'profitability', 'risk management', 'compliance']
            },
            'healthcare': {
                'keywords': ['patient', 'clinical', 'medical', 'healthcare', 'treatment', 'diagnosis', 'therapy'],
                'skills': ['EMR', 'HIPAA', 'clinical research', 'patient care', 'medical coding', 'ICD-10'],
                'metrics': ['patient outcomes', 'efficiency', 'quality', 'safety', 'compliance', 'satisfaction']
            }
        }
    
    async def analyze_resume_comprehensive(self, resume_data: Dict, job_description: str, 
                                         industry: str = 'technology') -> Dict[str, Any]:
        """Comprehensive resume analysis with advanced AI techniques"""
        
        start_time = datetime.now()
        
        # Extract text for analysis
        resume_text = self._extract_resume_text(resume_data)
        
        # Run parallel analysis tasks
        tasks = [
            self._analyze_ats_compatibility(resume_text, job_description),
            self._analyze_keyword_optimization(resume_text, job_description, industry),
            self._analyze_content_quality(resume_text, resume_data),
            self._analyze_quantifiable_achievements(resume_text),
            self._analyze_skills_alignment(resume_data, job_description, industry),
            self._analyze_experience_relevance(resume_data, job_description),
            self._analyze_format_structure(resume_data),
            self._analyze_readability(resume_text),
            self._analyze_impact_potential(resume_text, job_description)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        metrics = ResumeMetrics(
            ats_score=results[0] if not isinstance(results[0], Exception) else 0,
            keyword_density=results[1] if not isinstance(results[1], Exception) else 0,
            action_verb_usage=results[2] if not isinstance(results[2], Exception) else 0,
            quantifiable_achievements=results[3] if not isinstance(results[3], Exception) else 0,
            skills_relevance=results[4] if not isinstance(results[4], Exception) else 0,
            experience_alignment=results[5] if not isinstance(results[5], Exception) else 0,
            format_compatibility=results[6] if not isinstance(results[6], Exception) else 0,
            readability_score=results[7] if not isinstance(results[7], Exception) else 0,
            impact_score=results[8] if not isinstance(results[8], Exception) else 0,
            overall_score=0  # Will be calculated
        )
        
        # Calculate overall score
        metrics.overall_score = self._calculate_overall_score(metrics)
        
        # Generate enhancement suggestions
        suggestions = await self._generate_enhancement_suggestions(
            resume_data, job_description, metrics, industry
        )
        
        # Generate detailed analysis report
        analysis_report = self._generate_analysis_report(metrics, suggestions, industry)
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return {
            'metrics': {
                'ats_score': round(metrics.ats_score, 2),
                'keyword_density': round(metrics.keyword_density, 2),
                'action_verb_usage': round(metrics.action_verb_usage, 2),
                'quantifiable_achievements': round(metrics.quantifiable_achievements, 2),
                'skills_relevance': round(metrics.skills_relevance, 2),
                'experience_alignment': round(metrics.experience_alignment, 2),
                'format_compatibility': round(metrics.format_compatibility, 2),
                'readability_score': round(metrics.readability_score, 2),
                'impact_score': round(metrics.impact_score, 2),
                'overall_score': round(metrics.overall_score, 2)
            },
            'suggestions': suggestions,
            'analysis_report': analysis_report,
            'processing_time': round(processing_time, 2),
            'timestamp': datetime.now().isoformat()
        }
    
    async def _analyze_ats_compatibility(self, resume_text: str, job_description: str) -> float:
        """Analyze ATS compatibility with advanced pattern matching"""
        
        ats_score = 0
        total_checks = 0
        
        # Check for essential ATS elements
        for pattern_name, pattern in self.ats_patterns.items():
            if re.search(pattern, resume_text):
                ats_score += 10
            total_checks += 1
        
        # Check for proper formatting
        if self._check_ats_formatting(resume_text):
            ats_score += 20
        
        # Check for keyword density
        keyword_density = self._calculate_keyword_density(resume_text, job_description)
        ats_score += min(keyword_density * 2, 30)
        
        # Check for contact information completeness
        if self._check_contact_completeness(resume_text):
            ats_score += 15
        
        # Check for section completeness
        if self._check_section_completeness(resume_text):
            ats_score += 25
        
        return min(ats_score, 100)
    
    async def _analyze_keyword_optimization(self, resume_text: str, job_description: str, 
                                          industry: str) -> float:
        """Analyze keyword optimization with industry-specific weights"""
        
        # Extract keywords from job description
        job_keywords = self._extract_keywords_from_text(job_description)
        
        # Get industry-specific keywords
        industry_keywords = self.industry_weights.get(industry, {}).get('keywords', [])
        
        # Calculate keyword matches
        resume_lower = resume_text.lower()
        matches = 0
        total_keywords = len(job_keywords) + len(industry_keywords)
        
        for keyword in job_keywords + industry_keywords:
            if keyword.lower() in resume_lower:
                matches += 1
        
        if total_keywords == 0:
            return 0
        
        return (matches / total_keywords) * 100
    
    async def _analyze_content_quality(self, resume_text: str, resume_data: Dict) -> float:
        """Analyze content quality with AI-powered assessment"""
        
        # Check action verb usage
        action_verb_score = self._analyze_action_verb_usage(resume_text)
        
        # Check for quantified achievements
        quantified_score = self._analyze_quantified_content(resume_text)
        
        # Check for professional language
        professional_score = self._analyze_professional_language(resume_text)
        
        # Check for content completeness
        completeness_score = self._analyze_content_completeness(resume_data)
        
        return (action_verb_score + quantified_score + professional_score + completeness_score) / 4
    
    async def _analyze_quantifiable_achievements(self, resume_text: str) -> float:
        """Analyze quantifiable achievements with advanced pattern matching"""
        
        # Find all quantified achievements
        patterns = [
            r'\b\d+%',  # Percentages
            r'\$\d+[KMB]?',  # Money amounts
            r'\d+\+',  # Numbers with plus
            r'\d+x',  # Multipliers
            r'\d+\.\d+',  # Decimals
            r'\b\d+\s+(years?|months?|days?)\b',  # Time periods
            r'\b\d+\s+(people|employees|users|customers)\b'  # People counts
        ]
        
        matches = 0
        for pattern in patterns:
            matches += len(re.findall(pattern, resume_text, re.IGNORECASE))
        
        # Score based on number of quantified achievements
        if matches >= 10:
            return 100
        elif matches >= 7:
            return 80
        elif matches >= 5:
            return 60
        elif matches >= 3:
            return 40
        else:
            return 20
    
    async def _analyze_skills_alignment(self, resume_data: Dict, job_description: str, 
                                      industry: str) -> float:
        """Analyze skills alignment with job requirements"""
        
        resume_skills = self._extract_skills_from_resume(resume_data)
        job_skills = self._extract_skills_from_job_description(job_description)
        industry_skills = self.industry_weights.get(industry, {}).get('skills', [])
        
        # Calculate skill matches
        matches = 0
        total_skills = len(job_skills) + len(industry_skills)
        
        for skill in job_skills + industry_skills:
            if any(skill.lower() in resume_skill.lower() for resume_skill in resume_skills):
                matches += 1
        
        if total_skills == 0:
            return 0
        
        return (matches / total_skills) * 100
    
    async def _analyze_experience_relevance(self, resume_data: Dict, job_description: str) -> float:
        """Analyze experience relevance to job requirements"""
        
        experience = resume_data.get('experience', [])
        if not experience:
            return 0
        
        # Extract job requirements
        job_requirements = self._extract_job_requirements(job_description)
        
        relevant_experience = 0
        for exp in experience:
            exp_text = f"{exp.get('title', '')} {exp.get('company', '')} {exp.get('responsibilities', [])}"
            if any(req.lower() in exp_text.lower() for req in job_requirements):
                relevant_experience += 1
        
        return (relevant_experience / len(experience)) * 100
    
    async def _analyze_format_structure(self, resume_data: Dict) -> float:
        """Analyze resume format and structure"""
        
        score = 0
        
        # Check for essential sections
        essential_sections = ['contact', 'summary', 'experience', 'skills', 'education']
        for section in essential_sections:
            if section in resume_data and resume_data[section]:
                score += 20
        
        # Check for proper formatting
        if self._check_proper_formatting(resume_data):
            score += 20
        
        return min(score, 100)
    
    async def _analyze_readability(self, resume_text: str) -> float:
        """Analyze resume readability with advanced metrics"""
        
        # Calculate readability metrics
        sentences = re.split(r'[.!?]+', resume_text)
        words = resume_text.split()
        
        if len(sentences) == 0 or len(words) == 0:
            return 0
        
        # Average sentence length
        avg_sentence_length = len(words) / len(sentences)
        
        # Complex word ratio
        complex_words = [word for word in words if len(word) > 6]
        complex_word_ratio = len(complex_words) / len(words)
        
        # Calculate readability score
        readability_score = 100 - (avg_sentence_length * 2) - (complex_word_ratio * 50)
        
        return max(0, min(readability_score, 100))
    
    async def _analyze_impact_potential(self, resume_text: str, job_description: str) -> float:
        """Analyze potential impact and impression"""
        
        # Check for power words
        power_words = ['achieved', 'delivered', 'exceeded', 'surpassed', 'transformed', 'revolutionized']
        power_word_count = sum(1 for word in power_words if word.lower() in resume_text.lower())
        
        # Check for quantified achievements
        quantified_count = len(re.findall(r'\b\d+%|\$\d+|\d+\+|\d+x', resume_text))
        
        # Check for action verbs
        action_verb_count = len(re.findall(r'\b(led|managed|developed|created|improved|increased|reduced|optimized)', resume_text, re.IGNORECASE))
        
        # Calculate impact score
        impact_score = (power_word_count * 10) + (quantified_count * 5) + (action_verb_count * 3)
        
        return min(impact_score, 100)
    
    def _calculate_overall_score(self, metrics: ResumeMetrics) -> float:
        """Calculate weighted overall score"""
        
        weights = {
            'ats_score': 0.20,
            'keyword_density': 0.15,
            'action_verb_usage': 0.10,
            'quantifiable_achievements': 0.15,
            'skills_relevance': 0.15,
            'experience_alignment': 0.10,
            'format_compatibility': 0.05,
            'readability_score': 0.05,
            'impact_score': 0.05
        }
        
        overall_score = (
            metrics.ats_score * weights['ats_score'] +
            metrics.keyword_density * weights['keyword_density'] +
            metrics.action_verb_usage * weights['action_verb_usage'] +
            metrics.quantifiable_achievements * weights['quantifiable_achievements'] +
            metrics.skills_relevance * weights['skills_relevance'] +
            metrics.experience_alignment * weights['experience_alignment'] +
            metrics.format_compatibility * weights['format_compatibility'] +
            metrics.readability_score * weights['readability_score'] +
            metrics.impact_score * weights['impact_score']
        )
        
        return overall_score
    
    async def _generate_enhancement_suggestions(self, resume_data: Dict, job_description: str, 
                                              metrics: ResumeMetrics, industry: str) -> List[EnhancementSuggestion]:
        """Generate AI-powered enhancement suggestions"""
        
        suggestions = []
        
        # Generate suggestions based on low scores
        if metrics.ats_score < 70:
            suggestions.append(self._generate_ats_suggestion(resume_data, job_description))
        
        if metrics.keyword_density < 70:
            suggestions.append(self._generate_keyword_suggestion(resume_data, job_description, industry))
        
        if metrics.quantifiable_achievements < 60:
            suggestions.append(self._generate_quantification_suggestion(resume_data))
        
        if metrics.action_verb_usage < 70:
            suggestions.append(self._generate_action_verb_suggestion(resume_data))
        
        if metrics.skills_relevance < 70:
            suggestions.append(self._generate_skills_suggestion(resume_data, job_description, industry))
        
        if metrics.experience_alignment < 70:
            suggestions.append(self._generate_experience_suggestion(resume_data, job_description))
        
        return suggestions
    
    def _generate_ats_suggestion(self, resume_data: Dict, job_description: str) -> EnhancementSuggestion:
        """Generate ATS optimization suggestion"""
        
        return EnhancementSuggestion(
            category="ATS Optimization",
            priority="High",
            current_text="Current resume may not be ATS-friendly",
            suggested_text="Optimize for ATS compatibility",
            reasoning="Resume needs better formatting and keyword optimization for ATS systems",
            impact_score=85
        )
    
    def _generate_keyword_suggestion(self, resume_data: Dict, job_description: str, industry: str) -> EnhancementSuggestion:
        """Generate keyword optimization suggestion"""
        
        job_keywords = self._extract_keywords_from_text(job_description)
        industry_keywords = self.industry_weights.get(industry, {}).get('keywords', [])
        
        missing_keywords = []
        for keyword in job_keywords[:5] + industry_keywords[:5]:
            if keyword.lower() not in str(resume_data).lower():
                missing_keywords.append(keyword)
        
        return EnhancementSuggestion(
            category="Keyword Optimization",
            priority="High",
            current_text="Missing important keywords",
            suggested_text=f"Add keywords: {', '.join(missing_keywords[:3])}",
            reasoning="Resume needs more relevant keywords to match job requirements",
            impact_score=80
        )
    
    def _generate_quantification_suggestion(self, resume_data: Dict) -> EnhancementSuggestion:
        """Generate quantification suggestion"""
        
        return EnhancementSuggestion(
            category="Quantified Achievements",
            priority="Medium",
            current_text="Limited quantified achievements",
            suggested_text="Add specific numbers, percentages, and metrics",
            reasoning="Quantified achievements make resume more impactful and credible",
            impact_score=75
        )
    
    def _generate_action_verb_suggestion(self, resume_data: Dict) -> EnhancementSuggestion:
        """Generate action verb suggestion"""
        
        return EnhancementSuggestion(
            category="Action Verbs",
            priority="Medium",
            current_text="Weak action verb usage",
            suggested_text="Use stronger action verbs like 'Led', 'Delivered', 'Transformed'",
            reasoning="Strong action verbs make achievements more impactful",
            impact_score=70
        )
    
    def _generate_skills_suggestion(self, resume_data: Dict, job_description: str, industry: str) -> EnhancementSuggestion:
        """Generate skills alignment suggestion"""
        
        job_skills = self._extract_skills_from_job_description(job_description)
        industry_skills = self.industry_weights.get(industry, {}).get('skills', [])
        
        missing_skills = []
        for skill in job_skills[:3] + industry_skills[:3]:
            if skill.lower() not in str(resume_data).lower():
                missing_skills.append(skill)
        
        return EnhancementSuggestion(
            category="Skills Alignment",
            priority="High",
            current_text="Skills don't fully match job requirements",
            suggested_text=f"Add skills: {', '.join(missing_skills[:3])}",
            reasoning="Skills should align with job requirements and industry standards",
            impact_score=85
        )
    
    def _generate_experience_suggestion(self, resume_data: Dict, job_description: str) -> EnhancementSuggestion:
        """Generate experience alignment suggestion"""
        
        return EnhancementSuggestion(
            category="Experience Alignment",
            priority="Medium",
            current_text="Experience may not be fully relevant",
            suggested_text="Highlight relevant experience and achievements",
            reasoning="Experience should directly relate to job requirements",
            impact_score=70
        )
    
    def _generate_analysis_report(self, metrics: ResumeMetrics, suggestions: List[EnhancementSuggestion], 
                                industry: str) -> Dict[str, Any]:
        """Generate comprehensive analysis report"""
        
        # Determine overall grade
        if metrics.overall_score >= 90:
            grade = "A+"
        elif metrics.overall_score >= 85:
            grade = "A"
        elif metrics.overall_score >= 80:
            grade = "A-"
        elif metrics.overall_score >= 75:
            grade = "B+"
        elif metrics.overall_score >= 70:
            grade = "B"
        elif metrics.overall_score >= 65:
            grade = "B-"
        elif metrics.overall_score >= 60:
            grade = "C+"
        elif metrics.overall_score >= 55:
            grade = "C"
        else:
            grade = "D"
        
        # Generate strengths and weaknesses
        strengths = []
        weaknesses = []
        
        if metrics.ats_score >= 80:
            strengths.append("Strong ATS compatibility")
        else:
            weaknesses.append("Needs ATS optimization")
        
        if metrics.quantifiable_achievements >= 70:
            strengths.append("Good use of quantified achievements")
        else:
            weaknesses.append("Needs more quantified achievements")
        
        if metrics.skills_relevance >= 80:
            strengths.append("Skills align well with job requirements")
        else:
            weaknesses.append("Skills need better alignment")
        
        return {
            'overall_grade': grade,
            'strengths': strengths,
            'weaknesses': weaknesses,
            'priority_improvements': [s.category for s in suggestions if s.priority == "High"],
            'estimated_improvement': self._estimate_improvement_potential(metrics, suggestions),
            'industry_benchmark': self._get_industry_benchmark(industry),
            'next_steps': self._generate_next_steps(suggestions)
        }
    
    def _estimate_improvement_potential(self, metrics: ResumeMetrics, suggestions: List[EnhancementSuggestion]) -> float:
        """Estimate potential improvement score"""
        
        current_score = metrics.overall_score
        max_improvement = sum(s.impact_score for s in suggestions) / len(suggestions) if suggestions else 0
        
        potential_score = min(current_score + max_improvement, 100)
        return round(potential_score - current_score, 2)
    
    def _get_industry_benchmark(self, industry: str) -> Dict[str, Any]:
        """Get industry benchmark data"""
        
        benchmarks = {
            'technology': {'average_score': 78, 'top_percentile': 92},
            'finance': {'average_score': 82, 'top_percentile': 95},
            'healthcare': {'average_score': 75, 'top_percentile': 90}
        }
        
        return benchmarks.get(industry, {'average_score': 75, 'top_percentile': 90})
    
    def _generate_next_steps(self, suggestions: List[EnhancementSuggestion]) -> List[str]:
        """Generate actionable next steps"""
        
        next_steps = []
        
        for suggestion in suggestions[:3]:  # Top 3 suggestions
            next_steps.append(f"Focus on {suggestion.category}: {suggestion.suggested_text}")
        
        return next_steps
    
    # Helper methods
    def _extract_resume_text(self, resume_data: Dict) -> str:
        """Extract all text from resume data"""
        text_parts = []
        
        # Add summary
        if resume_data.get('summary'):
            text_parts.append(resume_data['summary'])
        
        # Add experience
        for exp in resume_data.get('experience', []):
            text_parts.append(exp.get('title', ''))
            text_parts.append(exp.get('company', ''))
            text_parts.extend(exp.get('responsibilities', []))
            text_parts.extend(exp.get('achievements', []))
        
        # Add skills
        skills = resume_data.get('skills', {})
        for skill_list in skills.values():
            if isinstance(skill_list, list):
                text_parts.extend(skill_list)
        
        return ' '.join(text_parts)
    
    def _extract_keywords_from_text(self, text: str) -> List[str]:
        """Extract keywords from text using NLP techniques"""
        # Simple keyword extraction - could be enhanced with NLP libraries
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        word_freq = Counter(words)
        return [word for word, freq in word_freq.most_common(20) if freq > 1]
    
    def _extract_skills_from_resume(self, resume_data: Dict) -> List[str]:
        """Extract skills from resume data"""
        skills = []
        
        skills_section = resume_data.get('skills', {})
        for skill_list in skills_section.values():
            if isinstance(skill_list, list):
                skills.extend(skill_list)
        
        return skills
    
    def _extract_skills_from_job_description(self, job_description: str) -> List[str]:
        """Extract skills from job description"""
        # Simple skill extraction - could be enhanced
        skills = []
        skill_keywords = ['Python', 'JavaScript', 'Java', 'C++', 'React', 'Angular', 'AWS', 'Docker', 'Kubernetes']
        
        for skill in skill_keywords:
            if skill.lower() in job_description.lower():
                skills.append(skill)
        
        return skills
    
    def _extract_job_requirements(self, job_description: str) -> List[str]:
        """Extract job requirements from job description"""
        # Simple requirement extraction - could be enhanced
        requirements = []
        req_keywords = ['experience', 'skills', 'knowledge', 'ability', 'required', 'must have']
        
        sentences = re.split(r'[.!?]+', job_description)
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in req_keywords):
                requirements.append(sentence.strip())
        
        return requirements
    
    def _check_ats_formatting(self, resume_text: str) -> bool:
        """Check if resume has ATS-friendly formatting"""
        # Check for common ATS issues
        issues = [
            'table' in resume_text.lower(),
            'image' in resume_text.lower(),
            'graphic' in resume_text.lower()
        ]
        
        return not any(issues)
    
    def _check_contact_completeness(self, resume_text: str) -> bool:
        """Check if contact information is complete"""
        contact_elements = ['email', 'phone', 'address']
        return all(element in resume_text.lower() for element in contact_elements)
    
    def _check_section_completeness(self, resume_text: str) -> bool:
        """Check if essential sections are present"""
        essential_sections = ['experience', 'skills', 'education']
        return all(section in resume_text.lower() for section in essential_sections)
    
    def _check_proper_formatting(self, resume_data: Dict) -> bool:
        """Check if resume has proper formatting"""
        # Check for proper data structure
        return all(key in resume_data for key in ['contact', 'experience', 'skills'])
    
    def _calculate_keyword_density(self, resume_text: str, job_description: str) -> float:
        """Calculate keyword density between resume and job description"""
        job_keywords = self._extract_keywords_from_text(job_description)
        resume_lower = resume_text.lower()
        
        matches = sum(1 for keyword in job_keywords if keyword.lower() in resume_lower)
        return (matches / len(job_keywords)) * 100 if job_keywords else 0
    
    def _analyze_action_verb_usage(self, resume_text: str) -> float:
        """Analyze action verb usage in resume"""
        all_action_verbs = []
        for verb_list in self.action_verbs.values():
            all_action_verbs.extend(verb_list)
        
        matches = sum(1 for verb in all_action_verbs if verb.lower() in resume_text.lower())
        return min((matches / len(all_action_verbs)) * 100, 100)
    
    def _analyze_quantified_content(self, resume_text: str) -> float:
        """Analyze quantified content in resume"""
        quantified_patterns = [r'\b\d+%', r'\$\d+', r'\d+\+', r'\d+x']
        matches = sum(len(re.findall(pattern, resume_text)) for pattern in quantified_patterns)
        
        if matches >= 10:
            return 100
        elif matches >= 7:
            return 80
        elif matches >= 5:
            return 60
        elif matches >= 3:
            return 40
        else:
            return 20
    
    def _analyze_professional_language(self, resume_text: str) -> float:
        """Analyze professional language usage"""
        # Check for professional language indicators
        professional_indicators = ['achieved', 'delivered', 'managed', 'developed', 'implemented']
        unprofessional_indicators = ['i', 'me', 'my', 'we', 'our']
        
        professional_count = sum(1 for indicator in professional_indicators if indicator in resume_text.lower())
        unprofessional_count = sum(1 for indicator in unprofessional_indicators if indicator in resume_text.lower())
        
        if unprofessional_count == 0:
            return 100
        else:
            return max(0, 100 - (unprofessional_count * 20))
    
    def _analyze_content_completeness(self, resume_data: Dict) -> float:
        """Analyze content completeness"""
        score = 0
        
        # Check for essential sections
        if resume_data.get('summary'):
            score += 20
        if resume_data.get('experience'):
            score += 30
        if resume_data.get('skills'):
            score += 20
        if resume_data.get('education'):
            score += 15
        if resume_data.get('projects'):
            score += 15
        
        return min(score, 100)

# Example usage
if __name__ == "__main__":
    analyzer = AdvancedResumeAnalyzer()
    
    # Sample resume data
    resume_data = {
        "summary": "Experienced software developer with expertise in Python and web development",
        "experience": [
            {
                "title": "Software Engineer",
                "company": "Tech Corp",
                "responsibilities": ["Developed web applications", "Managed databases"],
                "achievements": ["Improved performance by 30%", "Reduced bugs by 50%"]
            }
        ],
        "skills": {
            "technical": ["Python", "JavaScript", "React", "SQL"],
            "tools": ["Git", "Docker", "AWS"]
        },
        "education": [
            {
                "degree": "Bachelor of Computer Science",
                "institution": "University of Technology"
            }
        ]
    }
    
    job_description = "We are looking for a Python developer with React experience and AWS knowledge."
    
    # Run analysis
    import asyncio
    result = asyncio.run(analyzer.analyze_resume_comprehensive(resume_data, job_description))
    print(json.dumps(result, indent=2))
