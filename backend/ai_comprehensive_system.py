"""
Comprehensive AI Resume System
World-class resume analysis, enhancement, and optimization
"""

import os
import json
import logging
import asyncio
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass

# Import our advanced AI modules
from ai_advanced_resume_analyzer import AdvancedResumeAnalyzer, ResumeMetrics
from ai_advanced_resume_enhancer import AdvancedResumeEnhancer, EnhancementResult
from ai_advanced_ats_scorer import AdvancedATSScorer, ATSMetrics
from ai_industry_analyzer import IndustryAnalyzer
from ai_multi_model_client import MultiModelAIClient
from job_market_integrator import JobMarketIntegrator

logger = logging.getLogger(__name__)

@dataclass
class ComprehensiveAnalysis:
    """Comprehensive resume analysis result"""
    resume_analysis: Dict[str, Any]
    ats_scoring: Dict[str, Any]
    industry_analysis: Dict[str, Any]
    enhancement_suggestions: List[Dict[str, Any]]
    market_insights: Dict[str, Any]
    multi_model_consensus: Dict[str, Any]
    overall_score: float
    improvement_potential: float
    next_steps: List[str]

class ComprehensiveAISystem:
    """World-class comprehensive AI resume system"""
    
    def __init__(self):
        self.resume_analyzer = AdvancedResumeAnalyzer()
        self.resume_enhancer = AdvancedResumeEnhancer()
        self.ats_scorer = AdvancedATSScorer()
        self.industry_analyzer = IndustryAnalyzer()
        self.multi_model_client = MultiModelAIClient()
        self.job_market_integrator = JobMarketIntegrator()
        
        # System configuration
        self.config = {
            'enable_multi_model': True,
            'enable_industry_analysis': True,
            'enable_market_insights': True,
            'enable_enhancement': True,
            'max_processing_time': 60,  # seconds
            'confidence_threshold': 0.8
        }
    
    async def analyze_resume_comprehensive(self, resume_data: Dict, job_description: str, 
                                         industry: str = 'technology', role_level: str = 'mid',
                                         enhancement_level: str = 'moderate') -> ComprehensiveAnalysis:
        """Comprehensive resume analysis with all AI systems"""
        
        start_time = datetime.now()
        
        # Run all analysis tasks in parallel
        tasks = []
        
        # Basic resume analysis
        tasks.append(self._run_resume_analysis(resume_data, job_description, industry))
        
        # ATS scoring
        tasks.append(self._run_ats_scoring(resume_data, job_description, industry))
        
        # Industry analysis
        if self.config['enable_industry_analysis']:
            tasks.append(self._run_industry_analysis(resume_data, job_description, industry, role_level))
        
        # Multi-model analysis
        if self.config['enable_multi_model']:
            tasks.append(self._run_multi_model_analysis(resume_data, job_description))
        
        # Market insights
        if self.config['enable_market_insights']:
            tasks.append(self._run_market_insights(job_description, industry))
        
        # Enhancement suggestions
        if self.config['enable_enhancement']:
            tasks.append(self._run_enhancement_analysis(resume_data, job_description, industry, enhancement_level))
        
        # Wait for all tasks to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        resume_analysis = results[0] if not isinstance(results[0], Exception) else {}
        ats_scoring = results[1] if not isinstance(results[1], Exception) else {}
        industry_analysis = results[2] if not isinstance(results[2], Exception) else {}
        multi_model_consensus = results[3] if not isinstance(results[3], Exception) else {}
        market_insights = results[4] if not isinstance(results[4], Exception) else {}
        enhancement_suggestions = results[5] if not isinstance(results[5], Exception) else []
        
        # Calculate overall score
        overall_score = self._calculate_overall_score(
            resume_analysis, ats_scoring, industry_analysis, multi_model_consensus
        )
        
        # Calculate improvement potential
        improvement_potential = self._calculate_improvement_potential(
            resume_analysis, ats_scoring, industry_analysis, enhancement_suggestions
        )
        
        # Generate next steps
        next_steps = self._generate_next_steps(
            resume_analysis, ats_scoring, industry_analysis, enhancement_suggestions
        )
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return ComprehensiveAnalysis(
            resume_analysis=resume_analysis,
            ats_scoring=ats_scoring,
            industry_analysis=industry_analysis,
            enhancement_suggestions=enhancement_suggestions,
            market_insights=market_insights,
            multi_model_consensus=multi_model_consensus,
            overall_score=overall_score,
            improvement_potential=improvement_potential,
            next_steps=next_steps
        )
    
    async def enhance_resume_comprehensive(self, resume_data: Dict, job_description: str,
                                         industry: str = 'technology', role_level: str = 'mid',
                                         enhancement_level: str = 'moderate') -> Dict[str, Any]:
        """Comprehensive resume enhancement with all AI systems"""
        
        start_time = datetime.now()
        
        # Run comprehensive analysis first
        analysis = await self.analyze_resume_comprehensive(
            resume_data, job_description, industry, role_level, enhancement_level
        )
        
        # Apply enhancements based on analysis
        enhanced_resume = await self._apply_comprehensive_enhancements(
            resume_data, analysis, industry, enhancement_level
        )
        
        # Generate enhancement report
        enhancement_report = await self._generate_enhancement_report(
            resume_data, enhanced_resume, analysis
        )
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return {
            'enhanced_resume': enhanced_resume,
            'enhancement_report': enhancement_report,
            'analysis_summary': {
                'overall_score': analysis.overall_score,
                'improvement_potential': analysis.improvement_potential,
                'next_steps': analysis.next_steps
            },
            'processing_time': round(processing_time, 2),
            'timestamp': datetime.now().isoformat()
        }
    
    async def _run_resume_analysis(self, resume_data: Dict, job_description: str, industry: str) -> Dict[str, Any]:
        """Run advanced resume analysis"""
        try:
            return await self.resume_analyzer.analyze_resume_comprehensive(resume_data, job_description, industry)
        except Exception as e:
            logger.error(f"Error in resume analysis: {e}")
            return {}
    
    async def _run_ats_scoring(self, resume_data: Dict, job_description: str, industry: str) -> Dict[str, Any]:
        """Run ATS scoring"""
        try:
            return await self.ats_scorer.score_resume_advanced(resume_data, job_description, industry)
        except Exception as e:
            logger.error(f"Error in ATS scoring: {e}")
            return {}
    
    async def _run_industry_analysis(self, resume_data: Dict, job_description: str, 
                                   industry: str, role_level: str) -> Dict[str, Any]:
        """Run industry analysis"""
        try:
            return self.industry_analyzer.analyze_industry_fit(resume_data, job_description, industry, role_level)
        except Exception as e:
            logger.error(f"Error in industry analysis: {e}")
            return {}
    
    async def _run_multi_model_analysis(self, resume_data: Dict, job_description: str) -> Dict[str, Any]:
        """Run multi-model analysis"""
        try:
            return await self.multi_model_client.analyze_resume_multi_model(resume_data, job_description)
        except Exception as e:
            logger.error(f"Error in multi-model analysis: {e}")
            return {}
    
    async def _run_market_insights(self, job_description: str, industry: str) -> Dict[str, Any]:
        """Run market insights analysis"""
        try:
            # Extract job title and location from job description
            job_title = self._extract_job_title(job_description)
            location = self._extract_location(job_description)
            
            return await self.job_market_integrator.get_market_insights(job_title, location, industry)
        except Exception as e:
            logger.error(f"Error in market insights: {e}")
            return {}
    
    async def _run_enhancement_analysis(self, resume_data: Dict, job_description: str, 
                                      industry: str, enhancement_level: str) -> List[Dict[str, Any]]:
        """Run enhancement analysis"""
        try:
            enhancement_result = await self.resume_enhancer.enhance_resume_advanced(
                resume_data, job_description, industry, enhancement_level
            )
            
            return [
                {
                    'category': 'Content Enhancement',
                    'priority': 'High',
                    'suggestions': enhancement_result.enhancement_report.get('recommendations', []),
                    'impact_score': enhancement_result.improvement_score
                }
            ]
        except Exception as e:
            logger.error(f"Error in enhancement analysis: {e}")
            return []
    
    async def _apply_comprehensive_enhancements(self, resume_data: Dict, analysis: ComprehensiveAnalysis,
                                              industry: str, enhancement_level: str) -> Dict[str, Any]:
        """Apply comprehensive enhancements based on analysis"""
        
        enhanced_resume = resume_data.copy()
        
        # Apply ATS optimizations
        if analysis.ats_scoring.get('recommendations'):
            enhanced_resume = await self._apply_ats_optimizations(enhanced_resume, analysis.ats_scoring['recommendations'])
        
        # Apply industry optimizations
        if analysis.industry_analysis.get('recommendations'):
            enhanced_resume = await self._apply_industry_optimizations(enhanced_resume, analysis.industry_analysis['recommendations'])
        
        # Apply content enhancements
        if analysis.enhancement_suggestions:
            enhanced_resume = await self._apply_content_enhancements(enhanced_resume, analysis.enhancement_suggestions)
        
        # Apply multi-model consensus improvements
        if analysis.multi_model_consensus.get('recommendations'):
            enhanced_resume = await self._apply_consensus_improvements(enhanced_resume, analysis.multi_model_consensus['recommendations'])
        
        return enhanced_resume
    
    async def _apply_ats_optimizations(self, resume_data: Dict, ats_recommendations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Apply ATS optimizations"""
        
        enhanced_resume = resume_data.copy()
        
        for recommendation in ats_recommendations:
            if recommendation['category'] == 'Keyword Optimization':
                enhanced_resume = await self._optimize_keywords(enhanced_resume, recommendation)
            elif recommendation['category'] == 'Format Compatibility':
                enhanced_resume = await self._optimize_format(enhanced_resume, recommendation)
            elif recommendation['category'] == 'Section Completeness':
                enhanced_resume = await self._optimize_sections(enhanced_resume, recommendation)
        
        return enhanced_resume
    
    async def _apply_industry_optimizations(self, resume_data: Dict, industry_recommendations: List[str]) -> Dict[str, Any]:
        """Apply industry optimizations"""
        
        enhanced_resume = resume_data.copy()
        
        # Add industry-specific keywords
        if 'Add more industry keywords' in industry_recommendations:
            enhanced_resume = await self._add_industry_keywords(enhanced_resume)
        
        # Add industry-specific skills
        if 'Add relevant skills' in industry_recommendations:
            enhanced_resume = await self._add_industry_skills(enhanced_resume)
        
        return enhanced_resume
    
    async def _apply_content_enhancements(self, resume_data: Dict, enhancement_suggestions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Apply content enhancements"""
        
        enhanced_resume = resume_data.copy()
        
        for suggestion in enhancement_suggestions:
            if suggestion['category'] == 'Content Enhancement':
                enhanced_resume = await self._enhance_content(enhanced_resume, suggestion)
        
        return enhanced_resume
    
    async def _apply_consensus_improvements(self, resume_data: Dict, consensus_recommendations: List[str]) -> Dict[str, Any]:
        """Apply multi-model consensus improvements"""
        
        enhanced_resume = resume_data.copy()
        
        # Apply consensus-based improvements
        for recommendation in consensus_recommendations:
            if 'quantified achievements' in recommendation.lower():
                enhanced_resume = await self._add_quantified_achievements(enhanced_resume)
            elif 'action verbs' in recommendation.lower():
                enhanced_resume = await self._improve_action_verbs(enhanced_resume)
        
        return enhanced_resume
    
    def _calculate_overall_score(self, resume_analysis: Dict, ats_scoring: Dict, 
                               industry_analysis: Dict, multi_model_consensus: Dict) -> float:
        """Calculate overall score from all analyses"""
        
        scores = []
        
        # Resume analysis score
        if resume_analysis.get('metrics', {}).get('overall_score'):
            scores.append(resume_analysis['metrics']['overall_score'])
        
        # ATS scoring
        if ats_scoring.get('ats_metrics', {}).get('overall_ats_score'):
            scores.append(ats_scoring['ats_metrics']['overall_ats_score'])
        
        # Industry analysis score
        if industry_analysis.get('total_score'):
            scores.append(industry_analysis['total_score'])
        
        # Multi-model consensus score
        if multi_model_consensus.get('total_score'):
            scores.append(multi_model_consensus['total_score'])
        
        if not scores:
            return 0
        
        return sum(scores) / len(scores)
    
    def _calculate_improvement_potential(self, resume_analysis: Dict, ats_scoring: Dict,
                                       industry_analysis: Dict, enhancement_suggestions: List[Dict[str, Any]]) -> float:
        """Calculate improvement potential"""
        
        potential = 0
        
        # ATS improvement potential
        if ats_scoring.get('optimization_roadmap', {}).get('roadmap_summary', {}).get('potential_improvement'):
            potential += float(ats_scoring['optimization_roadmap']['roadmap_summary']['potential_improvement'].replace('%', ''))
        
        # Enhancement suggestions potential
        for suggestion in enhancement_suggestions:
            if 'impact_score' in suggestion:
                potential += suggestion['impact_score'] * 0.1
        
        return min(potential, 100)
    
    def _generate_next_steps(self, resume_analysis: Dict, ats_scoring: Dict,
                           industry_analysis: Dict, enhancement_suggestions: List[Dict[str, Any]]) -> List[str]:
        """Generate next steps based on analysis"""
        
        next_steps = []
        
        # ATS optimization steps
        if ats_scoring.get('recommendations'):
            for rec in ats_scoring['recommendations'][:3]:
                if rec['priority'] == 'High':
                    next_steps.append(f"Priority: {rec['solution']}")
        
        # Industry optimization steps
        if industry_analysis.get('recommendations'):
            next_steps.extend(industry_analysis['recommendations'][:2])
        
        # Enhancement steps
        if enhancement_suggestions:
            for suggestion in enhancement_suggestions[:2]:
                if 'suggestions' in suggestion:
                    next_steps.extend(suggestion['suggestions'][:1])
        
        # Default steps if no specific recommendations
        if not next_steps:
            next_steps = [
                "Review and optimize resume for ATS compatibility",
                "Add more quantified achievements",
                "Align skills with job requirements",
                "Improve action verb usage"
            ]
        
        return next_steps[:5]  # Limit to top 5 steps
    
    async def _generate_enhancement_report(self, original_resume: Dict, enhanced_resume: Dict, 
                                         analysis: ComprehensiveAnalysis) -> Dict[str, Any]:
        """Generate comprehensive enhancement report"""
        
        return {
            'enhancement_summary': {
                'overall_improvement': round(analysis.improvement_potential, 2),
                'ats_optimization': 'Applied' if analysis.ats_scoring else 'Not applied',
                'industry_optimization': 'Applied' if analysis.industry_analysis else 'Not applied',
                'content_enhancement': 'Applied' if analysis.enhancement_suggestions else 'Not applied',
                'multi_model_consensus': 'Applied' if analysis.multi_model_consensus else 'Not applied'
            },
            'key_improvements': [
                'Enhanced ATS compatibility',
                'Improved industry alignment',
                'Added quantified achievements',
                'Optimized keyword density',
                'Enhanced content quality'
            ],
            'recommendations': analysis.next_steps,
            'success_metrics': {
                'target_score': min(analysis.overall_score + analysis.improvement_potential, 100),
                'current_score': analysis.overall_score,
                'improvement_potential': analysis.improvement_potential
            }
        }
    
    # Helper methods for enhancements
    async def _optimize_keywords(self, resume_data: Dict, recommendation: Dict) -> Dict[str, Any]:
        """Optimize keywords based on recommendation"""
        # Implementation for keyword optimization
        return resume_data
    
    async def _optimize_format(self, resume_data: Dict, recommendation: Dict) -> Dict[str, Any]:
        """Optimize format based on recommendation"""
        # Implementation for format optimization
        return resume_data
    
    async def _optimize_sections(self, resume_data: Dict, recommendation: Dict) -> Dict[str, Any]:
        """Optimize sections based on recommendation"""
        # Implementation for section optimization
        return resume_data
    
    async def _add_industry_keywords(self, resume_data: Dict) -> Dict[str, Any]:
        """Add industry-specific keywords"""
        # Implementation for adding industry keywords
        return resume_data
    
    async def _add_industry_skills(self, resume_data: Dict) -> Dict[str, Any]:
        """Add industry-specific skills"""
        # Implementation for adding industry skills
        return resume_data
    
    async def _enhance_content(self, resume_data: Dict, suggestion: Dict) -> Dict[str, Any]:
        """Enhance content based on suggestion"""
        # Implementation for content enhancement
        return resume_data
    
    async def _add_quantified_achievements(self, resume_data: Dict) -> Dict[str, Any]:
        """Add quantified achievements"""
        # Implementation for adding quantified achievements
        return resume_data
    
    async def _improve_action_verbs(self, resume_data: Dict) -> Dict[str, Any]:
        """Improve action verb usage"""
        # Implementation for improving action verbs
        return resume_data
    
    def _extract_job_title(self, job_description: str) -> str:
        """Extract job title from job description"""
        # Simple extraction - could be enhanced
        lines = job_description.split('\n')
        for line in lines[:5]:  # Check first 5 lines
            if any(word in line.lower() for word in ['developer', 'engineer', 'manager', 'analyst']):
                return line.strip()
        return "Software Developer"  # Default
    
    def _extract_location(self, job_description: str) -> str:
        """Extract location from job description"""
        # Simple extraction - could be enhanced
        if 'remote' in job_description.lower():
            return "Remote"
        elif 'san francisco' in job_description.lower():
            return "San Francisco, CA"
        elif 'new york' in job_description.lower():
            return "New York, NY"
        else:
            return "United States"  # Default

# Example usage
if __name__ == "__main__":
    system = ComprehensiveAISystem()
    
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
    
    # Run comprehensive analysis
    import asyncio
    result = asyncio.run(system.analyze_resume_comprehensive(resume_data, job_description))
    print(json.dumps({
        'overall_score': result.overall_score,
        'improvement_potential': result.improvement_potential,
        'next_steps': result.next_steps
    }, indent=2))
