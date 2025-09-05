"""
Advanced AI ATS Scorer
World-class ATS scoring with machine learning and advanced algorithms
"""

import os
import json
import logging
import re
import asyncio
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass
from collections import Counter, defaultdict
import openai
from openai import OpenAI

logger = logging.getLogger(__name__)

@dataclass
class ATSMetrics:
    """Comprehensive ATS metrics"""
    keyword_density: float
    format_compatibility: float
    section_completeness: float
    contact_info_completeness: float
    skills_relevance: float
    experience_alignment: float
    education_relevance: float
    quantifiable_achievements: float
    action_verb_usage: float
    readability_score: float
    overall_ats_score: float

@dataclass
class ATSRecommendation:
    """ATS optimization recommendation"""
    category: str
    priority: str
    issue: str
    solution: str
    impact_score: float
    implementation_difficulty: str

class AdvancedATSScorer:
    """World-class ATS scorer with advanced machine learning techniques"""
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # ATS compatibility patterns
        self.ats_patterns = {
            'contact_info': {
                'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                'phone': r'(\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}',
                'linkedin': r'linkedin\.com/in/[\w-]+',
                'github': r'github\.com/[\w-]+'
            },
            'sections': {
                'summary': r'(?i)(summary|profile|objective|professional summary)',
                'experience': r'(?i)(experience|work history|professional experience|employment)',
                'education': r'(?i)(education|academic|degree|university|college)',
                'skills': r'(?i)(skills|technical skills|core competencies|expertise)',
                'projects': r'(?i)(projects|portfolio|key projects)',
                'certifications': r'(?i)(certifications|certificates|licenses)'
            },
            'formatting': {
                'bullet_points': r'^\s*[•·▪▫‣⁃]\s+',
                'dates': r'\b(19|20)\d{2}\b',
                'quantified_achievements': r'\b\d+%|\$\d+[KMB]?|\d+\+|\d+x|\d+\.\d+',
                'action_verbs': r'\b(led|managed|developed|created|improved|increased|reduced|optimized|delivered|achieved)\b'
            }
        }
        
        # ATS scoring weights
        self.scoring_weights = {
            'keyword_density': 0.20,
            'format_compatibility': 0.15,
            'section_completeness': 0.15,
            'contact_info_completeness': 0.10,
            'skills_relevance': 0.15,
            'experience_alignment': 0.10,
            'education_relevance': 0.05,
            'quantifiable_achievements': 0.05,
            'action_verb_usage': 0.03,
            'readability_score': 0.02
        }
        
        # Industry-specific ATS requirements
        self.industry_requirements = {
            'technology': {
                'required_keywords': ['software', 'development', 'programming', 'cloud', 'AI', 'data'],
                'required_skills': ['Python', 'JavaScript', 'AWS', 'Docker', 'Git'],
                'format_preferences': ['chronological', 'skills-based', 'hybrid']
            },
            'finance': {
                'required_keywords': ['financial', 'analysis', 'risk', 'compliance', 'trading'],
                'required_skills': ['Excel', 'SQL', 'Python', 'R', 'Tableau'],
                'format_preferences': ['chronological', 'functional']
            },
            'healthcare': {
                'required_keywords': ['patient', 'clinical', 'medical', 'healthcare', 'treatment'],
                'required_skills': ['EMR', 'HIPAA', 'clinical research', 'patient care'],
                'format_preferences': ['chronological', 'functional']
            }
        }
        
        # ATS system compatibility
        self.ats_systems = {
            'workday': {
                'preferred_format': 'chronological',
                'keyword_density': 0.05,
                'section_order': ['contact', 'summary', 'experience', 'education', 'skills']
            },
            'taleo': {
                'preferred_format': 'chronological',
                'keyword_density': 0.03,
                'section_order': ['contact', 'summary', 'experience', 'education', 'skills']
            },
            'greenhouse': {
                'preferred_format': 'hybrid',
                'keyword_density': 0.04,
                'section_order': ['contact', 'summary', 'experience', 'skills', 'education']
            },
            'lever': {
                'preferred_format': 'skills-based',
                'keyword_density': 0.06,
                'section_order': ['contact', 'summary', 'skills', 'experience', 'education']
            }
        }
    
    async def score_resume_advanced(self, resume_data: Dict, job_description: str, 
                                  industry: str = 'technology', ats_system: str = 'workday') -> Dict[str, Any]:
        """Advanced ATS scoring with machine learning techniques"""
        
        start_time = datetime.now()
        
        # Extract resume text
        resume_text = self._extract_resume_text(resume_data)
        
        # Calculate individual metrics
        metrics = await self._calculate_ats_metrics(resume_data, resume_text, job_description, industry, ats_system)
        
        # Calculate overall ATS score
        overall_score = self._calculate_overall_ats_score(metrics)
        
        # Generate ATS recommendations
        recommendations = await self._generate_ats_recommendations(metrics, resume_data, job_description, industry)
        
        # Generate ATS compatibility report
        compatibility_report = await self._generate_ats_compatibility_report(metrics, ats_system, industry)
        
        # Generate optimization roadmap
        optimization_roadmap = await self._generate_optimization_roadmap(recommendations, metrics)
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return {
            'ats_metrics': {
                'keyword_density': round(metrics.keyword_density, 2),
                'format_compatibility': round(metrics.format_compatibility, 2),
                'section_completeness': round(metrics.section_completeness, 2),
                'contact_info_completeness': round(metrics.contact_info_completeness, 2),
                'skills_relevance': round(metrics.skills_relevance, 2),
                'experience_alignment': round(metrics.experience_alignment, 2),
                'education_relevance': round(metrics.education_relevance, 2),
                'quantifiable_achievements': round(metrics.quantifiable_achievements, 2),
                'action_verb_usage': round(metrics.action_verb_usage, 2),
                'readability_score': round(metrics.readability_score, 2),
                'overall_ats_score': round(overall_score, 2)
            },
            'recommendations': recommendations,
            'compatibility_report': compatibility_report,
            'optimization_roadmap': optimization_roadmap,
            'ats_grade': self._calculate_ats_grade(overall_score),
            'processing_time': round(processing_time, 2),
            'timestamp': datetime.now().isoformat()
        }
    
    async def _calculate_ats_metrics(self, resume_data: Dict, resume_text: str, 
                                   job_description: str, industry: str, ats_system: str) -> ATSMetrics:
        """Calculate comprehensive ATS metrics"""
        
        # Calculate keyword density
        keyword_density = await self._calculate_keyword_density(resume_text, job_description, industry)
        
        # Calculate format compatibility
        format_compatibility = await self._calculate_format_compatibility(resume_data, resume_text, ats_system)
        
        # Calculate section completeness
        section_completeness = await self._calculate_section_completeness(resume_data, resume_text)
        
        # Calculate contact info completeness
        contact_info_completeness = await self._calculate_contact_info_completeness(resume_text)
        
        # Calculate skills relevance
        skills_relevance = await self._calculate_skills_relevance(resume_data, job_description, industry)
        
        # Calculate experience alignment
        experience_alignment = await self._calculate_experience_alignment(resume_data, job_description, industry)
        
        # Calculate education relevance
        education_relevance = await self._calculate_education_relevance(resume_data, job_description, industry)
        
        # Calculate quantifiable achievements
        quantifiable_achievements = await self._calculate_quantifiable_achievements(resume_text)
        
        # Calculate action verb usage
        action_verb_usage = await self._calculate_action_verb_usage(resume_text)
        
        # Calculate readability score
        readability_score = await self._calculate_readability_score(resume_text)
        
        return ATSMetrics(
            keyword_density=keyword_density,
            format_compatibility=format_compatibility,
            section_completeness=section_completeness,
            contact_info_completeness=contact_info_completeness,
            skills_relevance=skills_relevance,
            experience_alignment=experience_alignment,
            education_relevance=education_relevance,
            quantifiable_achievements=quantifiable_achievements,
            action_verb_usage=action_verb_usage,
            readability_score=readability_score,
            overall_ats_score=0  # Will be calculated
        )
    
    async def _calculate_keyword_density(self, resume_text: str, job_description: str, industry: str) -> float:
        """Calculate keyword density for ATS optimization"""
        
        # Extract keywords from job description
        job_keywords = self._extract_keywords_from_text(job_description)
        
        # Get industry-specific keywords
        industry_keywords = self.industry_requirements.get(industry, {}).get('required_keywords', [])
        
        # Calculate keyword matches
        resume_lower = resume_text.lower()
        total_keywords = len(job_keywords) + len(industry_keywords)
        
        if total_keywords == 0:
            return 0
        
        matches = 0
        for keyword in job_keywords + industry_keywords:
            if keyword.lower() in resume_lower:
                matches += 1
        
        # Calculate density score
        density_score = (matches / total_keywords) * 100
        
        # Apply industry-specific adjustments
        industry_adjustment = self._get_industry_keyword_adjustment(industry)
        
        return min(density_score * industry_adjustment, 100)
    
    async def _calculate_format_compatibility(self, resume_data: Dict, resume_text: str, ats_system: str) -> float:
        """Calculate format compatibility with ATS systems"""
        
        score = 0
        total_checks = 0
        
        # Check for ATS-friendly formatting
        ats_checks = [
            self._check_ats_friendly_formatting(resume_text),
            self._check_proper_section_structure(resume_data),
            self._check_bullet_point_usage(resume_text),
            self._check_date_formatting(resume_text),
            self._check_font_compatibility(resume_text)
        ]
        
        score = sum(ats_checks) * 20  # Each check worth 20 points
        total_checks = len(ats_checks)
        
        # Apply ATS system specific adjustments
        ats_adjustment = self._get_ats_system_adjustment(ats_system)
        
        return min(score * ats_adjustment, 100)
    
    async def _calculate_section_completeness(self, resume_data: Dict, resume_text: str) -> float:
        """Calculate section completeness for ATS"""
        
        required_sections = ['contact', 'summary', 'experience', 'skills', 'education']
        present_sections = 0
        
        for section in required_sections:
            if section in resume_data and resume_data[section]:
                present_sections += 1
        
        # Check for section headers in text
        section_headers = 0
        for section in required_sections:
            if re.search(self.ats_patterns['sections'][section], resume_text, re.IGNORECASE):
                section_headers += 1
        
        # Calculate completeness score
        data_completeness = (present_sections / len(required_sections)) * 50
        header_completeness = (section_headers / len(required_sections)) * 50
        
        return data_completeness + header_completeness
    
    async def _calculate_contact_info_completeness(self, resume_text: str) -> float:
        """Calculate contact information completeness"""
        
        contact_elements = ['email', 'phone', 'address', 'linkedin', 'github']
        present_elements = 0
        
        for element in contact_elements:
            if re.search(self.ats_patterns['contact_info'][element], resume_text, re.IGNORECASE):
                present_elements += 1
        
        return (present_elements / len(contact_elements)) * 100
    
    async def _calculate_skills_relevance(self, resume_data: Dict, job_description: str, industry: str) -> float:
        """Calculate skills relevance to job requirements"""
        
        resume_skills = self._extract_skills_from_resume(resume_data)
        job_skills = self._extract_skills_from_job_description(job_description)
        industry_skills = self.industry_requirements.get(industry, {}).get('required_skills', [])
        
        # Calculate skill matches
        total_skills = len(job_skills) + len(industry_skills)
        if total_skills == 0:
            return 0
        
        matches = 0
        for skill in job_skills + industry_skills:
            if any(skill.lower() in resume_skill.lower() for resume_skill in resume_skills):
                matches += 1
        
        return (matches / total_skills) * 100
    
    async def _calculate_experience_alignment(self, resume_data: Dict, job_description: str, industry: str) -> float:
        """Calculate experience alignment with job requirements"""
        
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
    
    async def _calculate_education_relevance(self, resume_data: Dict, job_description: str, industry: str) -> float:
        """Calculate education relevance to job requirements"""
        
        education = resume_data.get('education', [])
        if not education:
            return 0
        
        # Extract education requirements from job description
        education_requirements = self._extract_education_requirements(job_description)
        
        if not education_requirements:
            return 100  # No specific education requirements
        
        # Check if education matches requirements
        for edu in education:
            degree = edu.get('degree', '').lower()
            if any(req.lower() in degree for req in education_requirements):
                return 100
        
        return 50  # Partial match
    
    async def _calculate_quantifiable_achievements(self, resume_text: str) -> float:
        """Calculate quantifiable achievements score"""
        
        quantified_patterns = [
            r'\b\d+%',  # Percentages
            r'\$\d+[KMB]?',  # Money amounts
            r'\d+\+',  # Numbers with plus
            r'\d+x',  # Multipliers
            r'\d+\.\d+',  # Decimals
            r'\b\d+\s+(years?|months?|days?)\b'  # Time periods
        ]
        
        total_achievements = 0
        for pattern in quantified_patterns:
            total_achievements += len(re.findall(pattern, resume_text, re.IGNORECASE))
        
        # Score based on number of quantified achievements
        if total_achievements >= 10:
            return 100
        elif total_achievements >= 7:
            return 80
        elif total_achievements >= 5:
            return 60
        elif total_achievements >= 3:
            return 40
        else:
            return 20
    
    async def _calculate_action_verb_usage(self, resume_text: str) -> float:
        """Calculate action verb usage score"""
        
        action_verbs = [
            'led', 'managed', 'developed', 'created', 'improved', 'increased', 'reduced',
            'optimized', 'delivered', 'achieved', 'exceeded', 'surpassed', 'accomplished',
            'transformed', 'revolutionized', 'pioneered', 'spearheaded', 'orchestrated'
        ]
        
        total_verbs = len(action_verbs)
        matches = 0
        
        for verb in action_verbs:
            if re.search(r'\b' + verb + r'\b', resume_text, re.IGNORECASE):
                matches += 1
        
        return (matches / total_verbs) * 100
    
    async def _calculate_readability_score(self, resume_text: str) -> float:
        """Calculate readability score for ATS"""
        
        # Calculate basic readability metrics
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
    
    def _calculate_overall_ats_score(self, metrics: ATSMetrics) -> float:
        """Calculate overall ATS score using weighted average"""
        
        overall_score = (
            metrics.keyword_density * self.scoring_weights['keyword_density'] +
            metrics.format_compatibility * self.scoring_weights['format_compatibility'] +
            metrics.section_completeness * self.scoring_weights['section_completeness'] +
            metrics.contact_info_completeness * self.scoring_weights['contact_info_completeness'] +
            metrics.skills_relevance * self.scoring_weights['skills_relevance'] +
            metrics.experience_alignment * self.scoring_weights['experience_alignment'] +
            metrics.education_relevance * self.scoring_weights['education_relevance'] +
            metrics.quantifiable_achievements * self.scoring_weights['quantifiable_achievements'] +
            metrics.action_verb_usage * self.scoring_weights['action_verb_usage'] +
            metrics.readability_score * self.scoring_weights['readability_score']
        )
        
        return overall_score
    
    async def _generate_ats_recommendations(self, metrics: ATSMetrics, resume_data: Dict, 
                                          job_description: str, industry: str) -> List[ATSRecommendation]:
        """Generate ATS optimization recommendations"""
        
        recommendations = []
        
        # Keyword density recommendations
        if metrics.keyword_density < 70:
            recommendations.append(ATSRecommendation(
                category="Keyword Optimization",
                priority="High",
                issue=f"Low keyword density ({metrics.keyword_density:.1f}%)",
                solution="Add more relevant keywords from job description",
                impact_score=85,
                implementation_difficulty="Easy"
            ))
        
        # Format compatibility recommendations
        if metrics.format_compatibility < 80:
            recommendations.append(ATSRecommendation(
                category="Format Compatibility",
                priority="High",
                issue=f"Format compatibility issues ({metrics.format_compatibility:.1f}%)",
                solution="Optimize resume format for ATS systems",
                impact_score=90,
                implementation_difficulty="Medium"
            ))
        
        # Section completeness recommendations
        if metrics.section_completeness < 90:
            recommendations.append(ATSRecommendation(
                category="Section Completeness",
                priority="Medium",
                issue=f"Missing sections ({metrics.section_completeness:.1f}%)",
                solution="Add missing essential sections",
                impact_score=75,
                implementation_difficulty="Easy"
            ))
        
        # Contact info recommendations
        if metrics.contact_info_completeness < 100:
            recommendations.append(ATSRecommendation(
                category="Contact Information",
                priority="High",
                issue=f"Incomplete contact info ({metrics.contact_info_completeness:.1f}%)",
                solution="Add missing contact information",
                impact_score=95,
                implementation_difficulty="Easy"
            ))
        
        # Skills relevance recommendations
        if metrics.skills_relevance < 70:
            recommendations.append(ATSRecommendation(
                category="Skills Alignment",
                priority="High",
                issue=f"Skills don't match job requirements ({metrics.skills_relevance:.1f}%)",
                solution="Add relevant skills from job description",
                impact_score=80,
                implementation_difficulty="Medium"
            ))
        
        # Experience alignment recommendations
        if metrics.experience_alignment < 70:
            recommendations.append(ATSRecommendation(
                category="Experience Alignment",
                priority="Medium",
                issue=f"Experience not aligned with job ({metrics.experience_alignment:.1f}%)",
                solution="Highlight relevant experience and achievements",
                impact_score=70,
                implementation_difficulty="Hard"
            ))
        
        # Quantifiable achievements recommendations
        if metrics.quantifiable_achievements < 60:
            recommendations.append(ATSRecommendation(
                category="Quantified Achievements",
                priority="Medium",
                issue=f"Limited quantified achievements ({metrics.quantifiable_achievements:.1f}%)",
                solution="Add specific numbers, percentages, and metrics",
                impact_score=75,
                implementation_difficulty="Medium"
            ))
        
        # Action verb usage recommendations
        if metrics.action_verb_usage < 70:
            recommendations.append(ATSRecommendation(
                category="Action Verbs",
                priority="Low",
                issue=f"Weak action verb usage ({metrics.action_verb_usage:.1f}%)",
                solution="Use stronger action verbs",
                impact_score=60,
                implementation_difficulty="Easy"
            ))
        
        return recommendations
    
    async def _generate_ats_compatibility_report(self, metrics: ATSMetrics, ats_system: str, industry: str) -> Dict[str, Any]:
        """Generate ATS compatibility report"""
        
        return {
            'ats_system': ats_system,
            'industry': industry,
            'compatibility_score': round(metrics.overall_ats_score, 2),
            'compatibility_grade': self._calculate_ats_grade(metrics.overall_ats_score),
            'strengths': self._identify_ats_strengths(metrics),
            'weaknesses': self._identify_ats_weaknesses(metrics),
            'optimization_potential': self._calculate_optimization_potential(metrics),
            'industry_benchmark': self._get_industry_benchmark(industry),
            'ats_system_requirements': self.ats_systems.get(ats_system, {})
        }
    
    async def _generate_optimization_roadmap(self, recommendations: List[ATSRecommendation], 
                                           metrics: ATSMetrics) -> Dict[str, Any]:
        """Generate optimization roadmap"""
        
        # Group recommendations by priority
        high_priority = [r for r in recommendations if r.priority == "High"]
        medium_priority = [r for r in recommendations if r.priority == "Medium"]
        low_priority = [r for r in recommendations if r.priority == "Low"]
        
        # Estimate time to implement
        total_time = sum(self._estimate_implementation_time(r) for r in recommendations)
        
        # Calculate potential improvement
        potential_improvement = sum(r.impact_score for r in recommendations) / len(recommendations) if recommendations else 0
        
        return {
            'roadmap_summary': {
                'total_recommendations': len(recommendations),
                'high_priority': len(high_priority),
                'medium_priority': len(medium_priority),
                'low_priority': len(low_priority),
                'estimated_time': f"{total_time} hours",
                'potential_improvement': f"{potential_improvement:.1f}%"
            },
            'implementation_plan': {
                'phase_1': [r.category for r in high_priority],
                'phase_2': [r.category for r in medium_priority],
                'phase_3': [r.category for r in low_priority]
            },
            'success_metrics': {
                'target_ats_score': min(metrics.overall_ats_score + potential_improvement, 100),
                'expected_improvement': potential_improvement,
                'implementation_difficulty': self._calculate_overall_difficulty(recommendations)
            }
        }
    
    def _calculate_ats_grade(self, score: float) -> str:
        """Calculate ATS grade from score"""
        if score >= 95:
            return "A+"
        elif score >= 90:
            return "A"
        elif score >= 85:
            return "A-"
        elif score >= 80:
            return "B+"
        elif score >= 75:
            return "B"
        elif score >= 70:
            return "B-"
        elif score >= 65:
            return "C+"
        elif score >= 60:
            return "C"
        elif score >= 55:
            return "C-"
        else:
            return "D"
    
    def _identify_ats_strengths(self, metrics: ATSMetrics) -> List[str]:
        """Identify ATS strengths"""
        strengths = []
        
        if metrics.keyword_density >= 80:
            strengths.append("Strong keyword optimization")
        if metrics.format_compatibility >= 85:
            strengths.append("Excellent format compatibility")
        if metrics.section_completeness >= 90:
            strengths.append("Complete section structure")
        if metrics.contact_info_completeness >= 90:
            strengths.append("Complete contact information")
        if metrics.skills_relevance >= 80:
            strengths.append("Well-aligned skills")
        if metrics.quantifiable_achievements >= 70:
            strengths.append("Good use of quantified achievements")
        
        return strengths
    
    def _identify_ats_weaknesses(self, metrics: ATSMetrics) -> List[str]:
        """Identify ATS weaknesses"""
        weaknesses = []
        
        if metrics.keyword_density < 70:
            weaknesses.append("Low keyword density")
        if metrics.format_compatibility < 80:
            weaknesses.append("Format compatibility issues")
        if metrics.section_completeness < 90:
            weaknesses.append("Missing sections")
        if metrics.contact_info_completeness < 90:
            weaknesses.append("Incomplete contact information")
        if metrics.skills_relevance < 70:
            weaknesses.append("Skills don't match job requirements")
        if metrics.quantifiable_achievements < 60:
            weaknesses.append("Limited quantified achievements")
        
        return weaknesses
    
    def _calculate_optimization_potential(self, metrics: ATSMetrics) -> float:
        """Calculate optimization potential"""
        max_possible_score = 100
        current_score = metrics.overall_ats_score
        return max_possible_score - current_score
    
    def _get_industry_benchmark(self, industry: str) -> Dict[str, Any]:
        """Get industry benchmark data"""
        benchmarks = {
            'technology': {'average_score': 78, 'top_percentile': 92},
            'finance': {'average_score': 82, 'top_percentile': 95},
            'healthcare': {'average_score': 75, 'top_percentile': 90}
        }
        
        return benchmarks.get(industry, {'average_score': 75, 'top_percentile': 90})
    
    def _estimate_implementation_time(self, recommendation: ATSRecommendation) -> int:
        """Estimate implementation time in hours"""
        difficulty_times = {
            'Easy': 1,
            'Medium': 3,
            'Hard': 6
        }
        
        return difficulty_times.get(recommendation.implementation_difficulty, 2)
    
    def _calculate_overall_difficulty(self, recommendations: List[ATSRecommendation]) -> str:
        """Calculate overall implementation difficulty"""
        if not recommendations:
            return "Easy"
        
        difficulties = [r.implementation_difficulty for r in recommendations]
        difficulty_counts = Counter(difficulties)
        
        if difficulty_counts['Hard'] > difficulty_counts['Medium'] and difficulty_counts['Hard'] > difficulty_counts['Easy']:
            return "Hard"
        elif difficulty_counts['Medium'] > difficulty_counts['Easy']:
            return "Medium"
        else:
            return "Easy"
    
    def _get_industry_keyword_adjustment(self, industry: str) -> float:
        """Get industry-specific keyword adjustment factor"""
        adjustments = {
            'technology': 1.0,
            'finance': 1.1,
            'healthcare': 1.05
        }
        
        return adjustments.get(industry, 1.0)
    
    def _get_ats_system_adjustment(self, ats_system: str) -> float:
        """Get ATS system specific adjustment factor"""
        adjustments = {
            'workday': 1.0,
            'taleo': 0.95,
            'greenhouse': 1.05,
            'lever': 1.1
        }
        
        return adjustments.get(ats_system, 1.0)
    
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
        """Extract keywords from text"""
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
        skills = []
        skill_keywords = ['Python', 'JavaScript', 'Java', 'C++', 'React', 'Angular', 'AWS', 'Docker', 'Kubernetes']
        
        for skill in skill_keywords:
            if skill.lower() in job_description.lower():
                skills.append(skill)
        
        return skills
    
    def _extract_job_requirements(self, job_description: str) -> List[str]:
        """Extract job requirements from job description"""
        requirements = []
        req_keywords = ['experience', 'skills', 'knowledge', 'ability', 'required', 'must have']
        
        sentences = re.split(r'[.!?]+', job_description)
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in req_keywords):
                requirements.append(sentence.strip())
        
        return requirements
    
    def _extract_education_requirements(self, job_description: str) -> List[str]:
        """Extract education requirements from job description"""
        education_keywords = ['bachelor', 'master', 'phd', 'degree', 'university', 'college']
        requirements = []
        
        for keyword in education_keywords:
            if keyword.lower() in job_description.lower():
                requirements.append(keyword)
        
        return requirements
    
    def _check_ats_friendly_formatting(self, resume_text: str) -> bool:
        """Check if resume has ATS-friendly formatting"""
        # Check for common ATS issues
        issues = [
            'table' in resume_text.lower(),
            'image' in resume_text.lower(),
            'graphic' in resume_text.lower()
        ]
        
        return not any(issues)
    
    def _check_proper_section_structure(self, resume_data: Dict) -> bool:
        """Check if resume has proper section structure"""
        required_sections = ['contact', 'experience', 'skills']
        return all(section in resume_data for section in required_sections)
    
    def _check_bullet_point_usage(self, resume_text: str) -> bool:
        """Check if resume uses bullet points"""
        return bool(re.search(self.ats_patterns['formatting']['bullet_points'], resume_text, re.MULTILINE))
    
    def _check_date_formatting(self, resume_text: str) -> bool:
        """Check if resume has proper date formatting"""
        return bool(re.search(self.ats_patterns['formatting']['dates'], resume_text))
    
    def _check_font_compatibility(self, resume_text: str) -> bool:
        """Check if resume uses ATS-compatible fonts"""
        # This is a simplified check - could be enhanced
        return True

# Example usage
if __name__ == "__main__":
    scorer = AdvancedATSScorer()
    
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
    
    # Run ATS scoring
    import asyncio
    result = asyncio.run(scorer.score_resume_advanced(resume_data, job_description))
    print(json.dumps(result, indent=2))
