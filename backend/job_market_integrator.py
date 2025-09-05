"""
Job Market Integration System
Real-time job market data and insights
"""

import os
import json
import logging
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
import asyncio
import aiohttp

logger = logging.getLogger(__name__)

@dataclass
class JobMarketInsights:
    """Job market insights data structure"""
    salary_range: Dict[str, Any]
    skill_demand: Dict[str, float]
    competition_level: str
    trending_keywords: List[str]
    company_insights: Dict[str, Any]
    market_trends: Dict[str, Any]
    location_insights: Dict[str, Any]

class JobMarketIntegrator:
    """Real-time job market data integration"""
    
    def __init__(self):
        self.api_keys = {
            'indeed': os.getenv('INDEED_API_KEY'),
            'linkedin': os.getenv('LINKEDIN_API_KEY'),
            'glassdoor': os.getenv('GLASSDOOR_API_KEY'),
            'ziprecruiter': os.getenv('ZIPRECRUITER_API_KEY')
        }
        
        self.cache = {}
        self.cache_duration = 3600  # 1 hour cache
        
        # Industry salary data (fallback)
        self.salary_data = self._load_salary_data()
        
        # Skill demand data (fallback)
        self.skill_demand_data = self._load_skill_demand_data()
    
    def _load_salary_data(self) -> Dict[str, Dict[str, Any]]:
        """Load fallback salary data by industry and role"""
        return {
            'technology': {
                'software_engineer': {'min': 70000, 'max': 150000, 'median': 95000},
                'data_scientist': {'min': 80000, 'max': 160000, 'median': 110000},
                'devops_engineer': {'min': 90000, 'max': 170000, 'median': 120000},
                'product_manager': {'min': 100000, 'max': 180000, 'median': 130000}
            },
            'finance': {
                'financial_analyst': {'min': 60000, 'max': 120000, 'median': 80000},
                'investment_banker': {'min': 100000, 'max': 250000, 'median': 150000},
                'risk_manager': {'min': 80000, 'max': 140000, 'median': 105000}
            },
            'healthcare': {
                'healthcare_analyst': {'min': 55000, 'max': 100000, 'median': 75000},
                'clinical_researcher': {'min': 60000, 'max': 110000, 'median': 80000}
            }
        }
    
    def _load_skill_demand_data(self) -> Dict[str, float]:
        """Load fallback skill demand data"""
        return {
            'python': 0.85,
            'javascript': 0.80,
            'java': 0.75,
            'react': 0.70,
            'aws': 0.65,
            'docker': 0.60,
            'kubernetes': 0.55,
            'machine_learning': 0.50,
            'data_science': 0.45,
            'cybersecurity': 0.40
        }
    
    async def get_market_insights(self, job_title: str, location: str, 
                                industry: str) -> JobMarketInsights:
        """Get comprehensive market insights"""
        
        # Check cache first
        cache_key = f"{job_title}_{location}_{industry}"
        if cache_key in self.cache:
            cached_data = self.cache[cache_key]
            if datetime.now() - cached_data['timestamp'] < timedelta(seconds=self.cache_duration):
                return cached_data['data']
        
        # Fetch data from multiple sources
        tasks = [
            self._get_salary_data(job_title, location, industry),
            self._get_skill_demand(job_title, industry),
            self._get_competition_level(job_title, location),
            self._get_trending_keywords(industry),
            self._get_company_insights(industry, location),
            self._get_market_trends(industry),
            self._get_location_insights(location, industry)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        salary_range = results[0] if not isinstance(results[0], Exception) else self._get_fallback_salary(job_title, industry)
        skill_demand = results[1] if not isinstance(results[1], Exception) else self.skill_demand_data
        competition_level = results[2] if not isinstance(results[2], Exception) else "Medium"
        trending_keywords = results[3] if not isinstance(results[3], Exception) else []
        company_insights = results[4] if not isinstance(results[4], Exception) else {}
        market_trends = results[5] if not isinstance(results[5], Exception) else {}
        location_insights = results[6] if not isinstance(results[6], Exception) else {}
        
        insights = JobMarketInsights(
            salary_range=salary_range,
            skill_demand=skill_demand,
            competition_level=competition_level,
            trending_keywords=trending_keywords,
            company_insights=company_insights,
            market_trends=market_trends,
            location_insights=location_insights
        )
        
        # Cache the results
        self.cache[cache_key] = {
            'data': insights,
            'timestamp': datetime.now()
        }
        
        return insights
    
    async def _get_salary_data(self, job_title: str, location: str, industry: str) -> Dict[str, Any]:
        """Get salary data from multiple sources"""
        salary_data = {}
        
        # Try Indeed API
        if self.api_keys['indeed']:
            try:
                indeed_data = await self._fetch_indeed_salary(job_title, location)
                salary_data.update(indeed_data)
            except Exception as e:
                logger.warning(f"Indeed salary API failed: {e}")
        
        # Try Glassdoor API
        if self.api_keys['glassdoor']:
            try:
                glassdoor_data = await self._fetch_glassdoor_salary(job_title, location)
                salary_data.update(glassdoor_data)
            except Exception as e:
                logger.warning(f"Glassdoor salary API failed: {e}")
        
        # Fallback to internal data
        if not salary_data:
            salary_data = self._get_fallback_salary(job_title, industry)
        
        return salary_data
    
    async def _get_skill_demand(self, job_title: str, industry: str) -> Dict[str, float]:
        """Get skill demand data"""
        # This would integrate with job posting APIs
        # For now, return enhanced fallback data
        base_demand = self.skill_demand_data.copy()
        
        # Enhance based on job title
        if 'senior' in job_title.lower():
            for skill in base_demand:
                base_demand[skill] = min(1.0, base_demand[skill] * 1.2)
        elif 'junior' in job_title.lower() or 'entry' in job_title.lower():
            for skill in base_demand:
                base_demand[skill] = max(0.1, base_demand[skill] * 0.8)
        
        return base_demand
    
    async def _get_competition_level(self, job_title: str, location: str) -> str:
        """Get competition level for job title and location"""
        # This would analyze job posting frequency and application rates
        # For now, return based on common patterns
        
        high_competition_keywords = ['software engineer', 'data scientist', 'product manager']
        low_competition_keywords = ['devops', 'cybersecurity', 'machine learning engineer']
        
        job_lower = job_title.lower()
        
        if any(keyword in job_lower for keyword in high_competition_keywords):
            return "High"
        elif any(keyword in job_lower for keyword in low_competition_keywords):
            return "Low"
        else:
            return "Medium"
    
    async def _get_trending_keywords(self, industry: str) -> List[str]:
        """Get trending keywords for industry"""
        trending_keywords = {
            'technology': [
                'artificial intelligence', 'machine learning', 'cloud computing',
                'cybersecurity', 'devops', 'microservices', 'kubernetes',
                'react', 'python', 'aws', 'docker'
            ],
            'finance': [
                'fintech', 'blockchain', 'cryptocurrency', 'risk management',
                'compliance', 'regulatory', 'data analysis', 'quantitative'
            ],
            'healthcare': [
                'telemedicine', 'electronic health records', 'healthcare analytics',
                'patient care', 'clinical research', 'medical devices'
            ]
        }
        
        return trending_keywords.get(industry, trending_keywords['technology'])
    
    async def _get_company_insights(self, industry: str, location: str) -> Dict[str, Any]:
        """Get company insights for industry and location"""
        return {
            'top_companies': self._get_top_companies(industry, location),
            'company_sizes': self._get_company_size_distribution(industry),
            'remote_work_percentage': self._get_remote_work_percentage(industry),
            'benefits_trends': self._get_benefits_trends(industry)
        }
    
    async def _get_market_trends(self, industry: str) -> Dict[str, Any]:
        """Get market trends for industry"""
        return {
            'growth_rate': self._get_industry_growth_rate(industry),
            'hiring_trends': self._get_hiring_trends(industry),
            'skill_evolution': self._get_skill_evolution(industry),
            'job_market_health': self._get_job_market_health(industry)
        }
    
    async def _get_location_insights(self, location: str, industry: str) -> Dict[str, Any]:
        """Get location-specific insights"""
        return {
            'cost_of_living': self._get_cost_of_living(location),
            'job_density': self._get_job_density(location, industry),
            'salary_adjustment': self._get_salary_adjustment(location),
            'remote_work_availability': self._get_remote_work_availability(location, industry)
        }
    
    async def _fetch_indeed_salary(self, job_title: str, location: str) -> Dict[str, Any]:
        """Fetch salary data from Indeed API"""
        # This would make actual API calls to Indeed
        # For now, return mock data
        return {
            'min_salary': 70000,
            'max_salary': 120000,
            'median_salary': 90000,
            'source': 'indeed'
        }
    
    async def _fetch_glassdoor_salary(self, job_title: str, location: str) -> Dict[str, Any]:
        """Fetch salary data from Glassdoor API"""
        # This would make actual API calls to Glassdoor
        # For now, return mock data
        return {
            'min_salary': 75000,
            'max_salary': 125000,
            'median_salary': 95000,
            'source': 'glassdoor'
        }
    
    def _get_fallback_salary(self, job_title: str, industry: str) -> Dict[str, Any]:
        """Get fallback salary data"""
        industry_data = self.salary_data.get(industry, {})
        
        # Find closest matching job title
        job_lower = job_title.lower()
        for job_key, salary_info in industry_data.items():
            if any(word in job_lower for word in job_key.split('_')):
                return salary_info
        
        # Default fallback
        return {
            'min_salary': 50000,
            'max_salary': 100000,
            'median_salary': 70000,
            'source': 'fallback'
        }
    
    def _get_top_companies(self, industry: str, location: str) -> List[str]:
        """Get top companies in industry and location"""
        companies = {
            'technology': ['Google', 'Microsoft', 'Amazon', 'Apple', 'Meta', 'Netflix', 'Uber', 'Airbnb'],
            'finance': ['JPMorgan', 'Goldman Sachs', 'Morgan Stanley', 'BlackRock', 'Vanguard', 'Fidelity'],
            'healthcare': ['Johnson & Johnson', 'Pfizer', 'UnitedHealth', 'Anthem', 'Cigna', 'Aetna']
        }
        
        return companies.get(industry, companies['technology'])[:5]
    
    def _get_company_size_distribution(self, industry: str) -> Dict[str, float]:
        """Get company size distribution for industry"""
        return {
            'startup': 0.3,
            'small': 0.2,
            'medium': 0.3,
            'large': 0.2
        }
    
    def _get_remote_work_percentage(self, industry: str) -> float:
        """Get remote work percentage for industry"""
        remote_percentages = {
            'technology': 0.7,
            'finance': 0.4,
            'healthcare': 0.2,
            'consulting': 0.6
        }
        
        return remote_percentages.get(industry, 0.5)
    
    def _get_benefits_trends(self, industry: str) -> List[str]:
        """Get benefits trends for industry"""
        benefits = {
            'technology': ['Stock options', 'Flexible hours', 'Remote work', 'Learning budget'],
            'finance': ['Bonus structure', 'Health insurance', 'Retirement plan', 'Professional development'],
            'healthcare': ['Health insurance', 'Pension plan', 'Continuing education', 'Work-life balance']
        }
        
        return benefits.get(industry, ['Health insurance', 'Retirement plan', 'Professional development'])
    
    def _get_industry_growth_rate(self, industry: str) -> float:
        """Get industry growth rate"""
        growth_rates = {
            'technology': 0.15,
            'finance': 0.05,
            'healthcare': 0.08,
            'consulting': 0.06
        }
        
        return growth_rates.get(industry, 0.07)
    
    def _get_hiring_trends(self, industry: str) -> str:
        """Get hiring trends for industry"""
        return "Increasing"  # Placeholder
    
    def _get_skill_evolution(self, industry: str) -> List[str]:
        """Get skill evolution trends for industry"""
        skill_evolution = {
            'technology': ['AI/ML', 'Cloud computing', 'Cybersecurity', 'DevOps'],
            'finance': ['Fintech', 'Blockchain', 'Data analytics', 'Regulatory compliance'],
            'healthcare': ['Telemedicine', 'Health analytics', 'Digital health', 'Patient engagement']
        }
        
        return skill_evolution.get(industry, ['Digital transformation', 'Data analytics', 'Automation'])
    
    def _get_job_market_health(self, industry: str) -> str:
        """Get job market health for industry"""
        return "Strong"  # Placeholder
    
    def _get_cost_of_living(self, location: str) -> float:
        """Get cost of living index for location"""
        # This would integrate with cost of living APIs
        return 1.0  # Placeholder (1.0 = average)
    
    def _get_job_density(self, location: str, industry: str) -> float:
        """Get job density for location and industry"""
        return 0.8  # Placeholder (0.8 = high density)
    
    def _get_salary_adjustment(self, location: str) -> float:
        """Get salary adjustment factor for location"""
        return 1.0  # Placeholder (1.0 = no adjustment)
    
    def _get_remote_work_availability(self, location: str, industry: str) -> float:
        """Get remote work availability for location and industry"""
        return 0.6  # Placeholder (0.6 = 60% availability)

# Example usage
if __name__ == "__main__":
    integrator = JobMarketIntegrator()
    
    # Test market insights
    async def test_insights():
        insights = await integrator.get_market_insights(
            job_title="Software Engineer",
            location="San Francisco, CA",
            industry="technology"
        )
        
        print(json.dumps({
            'salary_range': insights.salary_range,
            'skill_demand': insights.skill_demand,
            'competition_level': insights.competition_level,
            'trending_keywords': insights.trending_keywords
        }, indent=2))
    
    asyncio.run(test_insights())
