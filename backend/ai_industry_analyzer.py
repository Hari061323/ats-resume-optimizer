"""
Industry-Specific Resume Analysis
Provides industry-optimized analysis and recommendations
"""

import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class IndustryProfile:
    """Industry-specific profile with keywords, skills, and metrics"""
    name: str
    keywords: List[str]
    skills: List[str]
    metrics: List[str]
    action_verbs: List[str]
    certifications: List[str]
    tools: List[str]
    experience_levels: Dict[str, int]

class IndustryAnalyzer:
    """Industry-specific resume analysis and optimization"""
    
    def __init__(self):
        self.industries = self._initialize_industries()
        self.role_levels = {
            'entry': {'min_experience': 0, 'max_experience': 2},
            'mid': {'min_experience': 2, 'max_experience': 5},
            'senior': {'min_experience': 5, 'max_experience': 10},
            'executive': {'min_experience': 10, 'max_experience': 20}
        }
    
    def _initialize_industries(self) -> Dict[str, IndustryProfile]:
        """Initialize industry profiles with specific requirements"""
        return {
            'technology': IndustryProfile(
                name='Technology',
                keywords=[
                    'software development', 'programming', 'cloud computing', 'artificial intelligence',
                    'machine learning', 'data science', 'cybersecurity', 'devops', 'agile', 'scrum',
                    'microservices', 'api development', 'database design', 'system architecture'
                ],
                skills=[
                    'Python', 'JavaScript', 'Java', 'C++', 'C#', 'Go', 'Rust', 'TypeScript',
                    'React', 'Angular', 'Vue.js', 'Node.js', 'Django', 'Flask', 'Spring',
                    'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Terraform',
                    'PostgreSQL', 'MongoDB', 'Redis', 'Elasticsearch', 'Kafka'
                ],
                metrics=[
                    'performance improvement', 'scalability', 'uptime', 'response time',
                    'code coverage', 'bug reduction', 'deployment frequency', 'user satisfaction',
                    'system reliability', 'cost optimization', 'security compliance'
                ],
                action_verbs=[
                    'Developed', 'Architected', 'Implemented', 'Deployed', 'Optimized',
                    'Scaled', 'Secured', 'Automated', 'Integrated', 'Migrated'
                ],
                certifications=[
                    'AWS Certified Solutions Architect', 'Google Cloud Professional',
                    'Microsoft Azure', 'CISSP', 'PMP', 'Scrum Master', 'ITIL'
                ],
                tools=[
                    'Git', 'Jenkins', 'Docker', 'Kubernetes', 'Terraform', 'Ansible',
                    'Prometheus', 'Grafana', 'ELK Stack', 'Jira', 'Confluence'
                ],
                experience_levels={'entry': 0, 'mid': 2, 'senior': 5, 'executive': 10}
            ),
            
            'finance': IndustryProfile(
                name='Finance',
                keywords=[
                    'financial analysis', 'risk management', 'compliance', 'trading',
                    'portfolio management', 'investment banking', 'corporate finance',
                    'audit', 'regulatory', 'derivatives', 'equity research', 'credit analysis'
                ],
                skills=[
                    'Excel', 'SQL', 'Python', 'R', 'SAS', 'Tableau', 'Power BI',
                    'VBA', 'Bloomberg Terminal', 'Reuters', 'FactSet', 'Morningstar',
                    'Financial Modeling', 'Valuation', 'Risk Assessment'
                ],
                metrics=[
                    'ROI', 'revenue growth', 'cost reduction', 'profitability',
                    'risk-adjusted returns', 'portfolio performance', 'compliance rate',
                    'audit findings', 'regulatory violations', 'client satisfaction'
                ],
                action_verbs=[
                    'Analyzed', 'Evaluated', 'Forecasted', 'Optimized', 'Managed',
                    'Monitored', 'Assessed', 'Implemented', 'Reduced', 'Increased'
                ],
                certifications=[
                    'CFA', 'CPA', 'FRM', 'CAIA', 'CIMA', 'ACCA', 'CISA'
                ],
                tools=[
                    'Bloomberg', 'Reuters', 'FactSet', 'Morningstar', 'S&P Capital IQ',
                    'Excel', 'Power BI', 'Tableau', 'SAS', 'R', 'Python'
                ],
                experience_levels={'entry': 0, 'mid': 3, 'senior': 6, 'executive': 12}
            ),
            
            'healthcare': IndustryProfile(
                name='Healthcare',
                keywords=[
                    'patient care', 'clinical research', 'medical devices', 'pharmaceuticals',
                    'healthcare IT', 'electronic health records', 'HIPAA', 'FDA compliance',
                    'clinical trials', 'medical coding', 'healthcare analytics', 'telemedicine'
                ],
                skills=[
                    'EMR Systems', 'Epic', 'Cerner', 'Allscripts', 'HIPAA Compliance',
                    'Medical Coding', 'ICD-10', 'CPT', 'Clinical Research', 'Data Analysis',
                    'Python', 'R', 'SAS', 'SQL', 'Tableau', 'Power BI'
                ],
                metrics=[
                    'patient outcomes', 'quality scores', 'safety metrics', 'efficiency',
                    'compliance rate', 'cost per patient', 'readmission rate', 'satisfaction scores'
                ],
                action_verbs=[
                    'Improved', 'Enhanced', 'Implemented', 'Monitored', 'Analyzed',
                    'Coordinated', 'Managed', 'Developed', 'Optimized', 'Reduced'
                ],
                certifications=[
                    'RN', 'MD', 'PharmD', 'RHIA', 'RHIT', 'CCS', 'CPC', 'PMP'
                ],
                tools=[
                    'Epic', 'Cerner', 'Allscripts', 'Meditech', 'NextGen',
                    'Tableau', 'Power BI', 'SAS', 'R', 'Python', 'SQL'
                ],
                experience_levels={'entry': 0, 'mid': 2, 'senior': 5, 'executive': 8}
            ),
            
            'marketing': IndustryProfile(
                name='Marketing',
                keywords=[
                    'digital marketing', 'content marketing', 'social media', 'SEO',
                    'SEM', 'email marketing', 'brand management', 'campaign management',
                    'analytics', 'conversion optimization', 'lead generation', 'customer acquisition'
                ],
                skills=[
                    'Google Analytics', 'Google Ads', 'Facebook Ads', 'LinkedIn Ads',
                    'HubSpot', 'Salesforce', 'Mailchimp', 'Hootsuite', 'Buffer',
                    'Adobe Creative Suite', 'Canva', 'Figma', 'WordPress', 'HTML/CSS'
                ],
                metrics=[
                    'ROI', 'conversion rate', 'click-through rate', 'engagement rate',
                    'cost per acquisition', 'customer lifetime value', 'brand awareness',
                    'lead generation', 'revenue attribution', 'campaign performance'
                ],
                action_verbs=[
                    'Increased', 'Generated', 'Optimized', 'Launched', 'Managed',
                    'Developed', 'Analyzed', 'Improved', 'Created', 'Executed'
                ],
                certifications=[
                    'Google Analytics', 'Google Ads', 'HubSpot', 'Facebook Blueprint',
                    'Hootsuite', 'PMP', 'Scrum Master'
                ],
                tools=[
                    'Google Analytics', 'Google Ads', 'Facebook Ads', 'LinkedIn Ads',
                    'HubSpot', 'Salesforce', 'Mailchimp', 'Hootsuite', 'Buffer',
                    'Adobe Creative Suite', 'Canva', 'Figma'
                ],
                experience_levels={'entry': 0, 'mid': 2, 'senior': 4, 'executive': 8}
            ),
            
            'consulting': IndustryProfile(
                name='Consulting',
                keywords=[
                    'strategy consulting', 'management consulting', 'business analysis',
                    'process improvement', 'change management', 'project management',
                    'client engagement', 'stakeholder management', 'problem solving',
                    'data analysis', 'market research', 'competitive analysis'
                ],
                skills=[
                    'PowerPoint', 'Excel', 'Tableau', 'Power BI', 'SQL', 'Python',
                    'R', 'SAS', 'SPSS', 'Project Management', 'Agile', 'Scrum',
                    'Business Analysis', 'Process Mapping', 'Financial Modeling'
                ],
                metrics=[
                    'client satisfaction', 'project success rate', 'cost savings',
                    'revenue growth', 'efficiency improvement', 'time to market',
                    'ROI', 'NPS score', 'engagement rate', 'delivery quality'
                ],
                action_verbs=[
                    'Analyzed', 'Developed', 'Implemented', 'Improved', 'Optimized',
                    'Managed', 'Led', 'Delivered', 'Transformed', 'Streamlined'
                ],
                certifications=[
                    'PMP', 'Scrum Master', 'Six Sigma', 'Lean', 'CBAP', 'PMP',
                    'CFA', 'CPA', 'MBA'
                ],
                tools=[
                    'PowerPoint', 'Excel', 'Tableau', 'Power BI', 'SQL', 'Python',
                    'R', 'SAS', 'SPSS', 'Jira', 'Confluence', 'Slack'
                ],
                experience_levels={'entry': 0, 'mid': 3, 'senior': 6, 'executive': 10}
            ),
            
            'education': IndustryProfile(
                name='Education',
                keywords=[
                    'curriculum development', 'instructional design', 'educational technology',
                    'student assessment', 'learning management systems', 'online learning',
                    'academic research', 'teaching', 'mentoring', 'professional development',
                    'educational policy', 'student success', 'academic excellence'
                ],
                skills=[
                    'LMS Systems', 'Moodle', 'Blackboard', 'Canvas', 'Google Classroom',
                    'PowerPoint', 'Prezi', 'Camtasia', 'Articulate', 'Storyline',
                    'Python', 'R', 'SPSS', 'Excel', 'Tableau', 'Power BI'
                ],
                metrics=[
                    'student success rate', 'course completion rate', 'student satisfaction',
                    'learning outcomes', 'engagement metrics', 'retention rate',
                    'graduation rate', 'academic performance', 'skill development'
                ],
                action_verbs=[
                    'Developed', 'Designed', 'Implemented', 'Improved', 'Enhanced',
                    'Mentored', 'Guided', 'Facilitated', 'Assessed', 'Evaluated'
                ],
                certifications=[
                    'Teaching License', 'EdD', 'PhD', 'PMP', 'Scrum Master',
                    'Google Certified Educator', 'Microsoft Certified Educator'
                ],
                tools=[
                    'LMS Systems', 'Moodle', 'Blackboard', 'Canvas', 'Google Classroom',
                    'PowerPoint', 'Prezi', 'Camtasia', 'Articulate', 'Storyline'
                ],
                experience_levels={'entry': 0, 'mid': 3, 'senior': 6, 'executive': 10}
            )
        }
    
    def analyze_industry_fit(self, resume_data: Dict, job_analysis: Dict, 
                           industry: str, role_level: str) -> Dict[str, Any]:
        """Analyze how well resume fits specific industry and role level"""
        
        if industry not in self.industries:
            industry = 'technology'  # Default fallback
        
        industry_profile = self.industries[industry]
        
        # Calculate industry-specific scores
        scores = {
            'keyword_match': self._score_keyword_match(resume_data, industry_profile),
            'skills_alignment': self._score_skills_alignment(resume_data, industry_profile),
            'experience_relevance': self._score_experience_relevance(resume_data, industry_profile, role_level),
            'certification_match': self._score_certification_match(resume_data, industry_profile),
            'tool_proficiency': self._score_tool_proficiency(resume_data, industry_profile),
            'metric_usage': self._score_metric_usage(resume_data, industry_profile)
        }
        
        # Calculate weighted total score
        weights = {
            'keyword_match': 0.25,
            'skills_alignment': 0.20,
            'experience_relevance': 0.20,
            'certification_match': 0.15,
            'tool_proficiency': 0.10,
            'metric_usage': 0.10
        }
        
        total_score = sum(scores[key] * weights[key] for key in scores)
        
        # Generate industry-specific recommendations
        recommendations = self._generate_industry_recommendations(
            resume_data, industry_profile, scores, role_level
        )
        
        # Calculate industry fit percentage
        fit_percentage = self._calculate_industry_fit(resume_data, industry_profile, role_level)
        
        return {
            'industry': industry,
            'role_level': role_level,
            'total_score': round(total_score, 2),
            'fit_percentage': round(fit_percentage, 2),
            'component_scores': {k: round(v, 2) for k, v in scores.items()},
            'recommendations': recommendations,
            'industry_keywords_missing': self._find_missing_keywords(resume_data, industry_profile),
            'industry_skills_missing': self._find_missing_skills(resume_data, industry_profile),
            'suggested_certifications': self._suggest_certifications(resume_data, industry_profile),
            'industry_metrics': self._suggest_metrics(resume_data, industry_profile),
            'action_verbs': industry_profile.action_verbs,
            'tools': industry_profile.tools,
            'analysis_timestamp': datetime.now().isoformat()
        }
    
    def _score_keyword_match(self, resume_data: Dict, industry_profile: IndustryProfile) -> float:
        """Score keyword matching for industry"""
        resume_text = self._extract_text_from_resume(resume_data)
        industry_keywords = industry_profile.keywords
        
        matches = 0
        for keyword in industry_keywords:
            if keyword.lower() in resume_text.lower():
                matches += 1
        
        return (matches / len(industry_keywords)) * 100
    
    def _score_skills_alignment(self, resume_data: Dict, industry_profile: IndustryProfile) -> float:
        """Score skills alignment with industry requirements"""
        resume_skills = resume_data.get('skills', {})
        all_skills = []
        
        for skill_category in resume_skills.values():
            if isinstance(skill_category, list):
                all_skills.extend(skill_category)
        
        industry_skills = industry_profile.skills
        matches = 0
        
        for skill in industry_skills:
            if any(skill.lower() in resume_skill.lower() for resume_skill in all_skills):
                matches += 1
        
        return (matches / len(industry_skills)) * 100
    
    def _score_experience_relevance(self, resume_data: Dict, industry_profile: IndustryProfile, 
                                  role_level: str) -> float:
        """Score experience relevance for industry and role level"""
        experience = resume_data.get('experience', [])
        if not experience:
            return 0
        
        # Check if experience is in relevant industry
        industry_keywords = industry_profile.keywords
        relevant_experience = 0
        
        for exp in experience:
            exp_text = f"{exp.get('title', '')} {exp.get('company', '')} {exp.get('responsibilities', [])}"
            if any(keyword.lower() in exp_text.lower() for keyword in industry_keywords):
                relevant_experience += 1
        
        # Check role level appropriateness
        total_years = self._calculate_total_experience(experience)
        expected_years = industry_profile.experience_levels.get(role_level, 0)
        
        if total_years >= expected_years:
            experience_score = 100
        else:
            experience_score = (total_years / expected_years) * 100
        
        return (relevant_experience / len(experience)) * 0.7 + experience_score * 0.3
    
    def _score_certification_match(self, resume_data: Dict, industry_profile: IndustryProfile) -> float:
        """Score certification match with industry requirements"""
        certifications = resume_data.get('certifications', [])
        if not certifications:
            return 0
        
        industry_certs = industry_profile.certifications
        matches = 0
        
        for cert in certifications:
            cert_name = cert.get('name', '') if isinstance(cert, dict) else str(cert)
            if any(industry_cert.lower() in cert_name.lower() for industry_cert in industry_certs):
                matches += 1
        
        return (matches / len(industry_certs)) * 100
    
    def _score_tool_proficiency(self, resume_data: Dict, industry_profile: IndustryProfile) -> float:
        """Score tool proficiency for industry"""
        resume_text = self._extract_text_from_resume(resume_data)
        industry_tools = industry_profile.tools
        
        matches = 0
        for tool in industry_tools:
            if tool.lower() in resume_text.lower():
                matches += 1
        
        return (matches / len(industry_tools)) * 100
    
    def _score_metric_usage(self, resume_data: Dict, industry_profile: IndustryProfile) -> float:
        """Score usage of industry-relevant metrics"""
        resume_text = self._extract_text_from_resume(resume_data)
        industry_metrics = industry_profile.metrics
        
        matches = 0
        for metric in industry_metrics:
            if metric.lower() in resume_text.lower():
                matches += 1
        
        return (matches / len(industry_metrics)) * 100
    
    def _extract_text_from_resume(self, resume_data: Dict) -> str:
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
        
        # Add projects
        for project in resume_data.get('projects', []):
            text_parts.append(project.get('name', ''))
            text_parts.append(project.get('description', ''))
            text_parts.extend(project.get('technologies', []))
        
        return ' '.join(text_parts)
    
    def _calculate_total_experience(self, experience: List[Dict]) -> int:
        """Calculate total years of experience"""
        total_years = 0
        for exp in experience:
            duration = exp.get('duration', '')
            # Simple parsing - could be enhanced
            if 'year' in duration.lower():
                try:
                    years = int(duration.split()[0])
                    total_years += years
                except:
                    pass
        return total_years
    
    def _generate_industry_recommendations(self, resume_data: Dict, industry_profile: IndustryProfile,
                                         scores: Dict, role_level: str) -> List[str]:
        """Generate industry-specific recommendations"""
        recommendations = []
        
        if scores['keyword_match'] < 70:
            recommendations.append(f"Add more {industry_profile.name.lower()} industry keywords")
        
        if scores['skills_alignment'] < 70:
            missing_skills = self._find_missing_skills(resume_data, industry_profile)[:3]
            recommendations.append(f"Develop skills in: {', '.join(missing_skills)}")
        
        if scores['certification_match'] < 50:
            recommendations.append(f"Consider obtaining industry certifications: {', '.join(industry_profile.certifications[:3])}")
        
        if scores['tool_proficiency'] < 60:
            recommendations.append(f"Learn industry tools: {', '.join(industry_profile.tools[:3])}")
        
        if scores['metric_usage'] < 50:
            recommendations.append("Include more quantifiable metrics and achievements")
        
        if scores['experience_relevance'] < 70:
            recommendations.append(f"Gain more experience in {industry_profile.name.lower()} industry")
        
        return recommendations
    
    def _find_missing_keywords(self, resume_data: Dict, industry_profile: IndustryProfile) -> List[str]:
        """Find missing industry keywords"""
        resume_text = self._extract_text_from_resume(resume_data)
        missing = []
        
        for keyword in industry_profile.keywords:
            if keyword.lower() not in resume_text.lower():
                missing.append(keyword)
        
        return missing[:5]  # Return top 5 missing keywords
    
    def _find_missing_skills(self, resume_data: Dict, industry_profile: IndustryProfile) -> List[str]:
        """Find missing industry skills"""
        resume_skills = resume_data.get('skills', {})
        all_skills = []
        
        for skill_category in resume_skills.values():
            if isinstance(skill_category, list):
                all_skills.extend(skill_category)
        
        missing = []
        for skill in industry_profile.skills:
            if not any(skill.lower() in resume_skill.lower() for resume_skill in all_skills):
                missing.append(skill)
        
        return missing[:5]  # Return top 5 missing skills
    
    def _suggest_certifications(self, resume_data: Dict, industry_profile: IndustryProfile) -> List[str]:
        """Suggest relevant certifications"""
        return industry_profile.certifications[:3]
    
    def _suggest_metrics(self, resume_data: Dict, industry_profile: IndustryProfile) -> List[str]:
        """Suggest relevant metrics to include"""
        return industry_profile.metrics[:5]
    
    def _calculate_industry_fit(self, resume_data: Dict, industry_profile: IndustryProfile, 
                              role_level: str) -> float:
        """Calculate overall industry fit percentage"""
        # This is a simplified calculation - could be enhanced
        return 75.0  # Placeholder

# Example usage
if __name__ == "__main__":
    analyzer = IndustryAnalyzer()
    
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
        }
    }
    
    job_analysis = {
        "industry": "technology",
        "role_level": "mid",
        "required_skills": ["Python", "React", "AWS"]
    }
    
    result = analyzer.analyze_industry_fit(
        resume_data, 
        job_analysis, 
        "technology", 
        "mid"
    )
    
    print(json.dumps(result, indent=2))
