"""
Multi-Model AI Client for Advanced Resume Analysis
Supports multiple AI models for consensus-based analysis
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import asyncio
from dataclasses import dataclass

# Import existing AI modules
from ai_resume_parser import AIResumeParser
from ai_keyword_analyzer import AIKeywordAnalyzer
from ai_ats_scorer import AIATSScorer

# Configure logging
logger = logging.getLogger(__name__)

@dataclass
class ModelResult:
    """Result from a single AI model"""
    model_name: str
    score: float
    confidence: float
    analysis: Dict[str, Any]
    processing_time: float
    cost: float
    error: Optional[str] = None

class MultiModelAIClient:
    """Unified client for multiple AI models with consensus analysis"""
    
    def __init__(self):
        self.models = {}
        self.model_weights = {
            'gpt4': 0.4,
            'gpt35': 0.3,
            'claude': 0.2,
            'gemini': 0.1
        }
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize all available AI models"""
        try:
            # GPT-4 (Primary model)
            if os.getenv('OPENAI_API_KEY'):
                self.models['gpt4'] = {
                    'client': self._create_openai_client('gpt-4-turbo'),
                    'weight': 0.4,
                    'max_tokens': 4000,
                    'temperature': 0.3
                }
            
            # GPT-3.5 (Fallback model)
            if os.getenv('OPENAI_API_KEY'):
                self.models['gpt35'] = {
                    'client': self._create_openai_client('gpt-3.5-turbo'),
                    'weight': 0.3,
                    'max_tokens': 2000,
                    'temperature': 0.5
                }
            
            # Claude (Anthropic)
            if os.getenv('ANTHROPIC_API_KEY'):
                self.models['claude'] = {
                    'client': self._create_claude_client(),
                    'weight': 0.2,
                    'max_tokens': 3000,
                    'temperature': 0.4
                }
            
            # Gemini (Google)
            if os.getenv('GOOGLE_API_KEY'):
                self.models['gemini'] = {
                    'client': self._create_gemini_client(),
                    'weight': 0.1,
                    'max_tokens': 2000,
                    'temperature': 0.6
                }
            
            logger.info(f"Initialized {len(self.models)} AI models: {list(self.models.keys())}")
            
        except Exception as e:
            logger.error(f"Error initializing AI models: {str(e)}")
    
    def _create_openai_client(self, model: str):
        """Create OpenAI client for specific model"""
        from openai import OpenAI
        return OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    def _create_claude_client(self):
        """Create Claude client"""
        try:
            import anthropic
            return anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        except ImportError:
            logger.warning("Anthropic package not installed")
            return None
    
    def _create_gemini_client(self):
        """Create Gemini client"""
        try:
            import google.generativeai as genai
            genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
            return genai.GenerativeModel('gemini-pro')
        except ImportError:
            logger.warning("Google Generative AI package not installed")
            return None
    
    async def analyze_resume_multi_model(self, resume_data: Dict, job_analysis: Dict) -> Dict[str, Any]:
        """Run analysis across multiple models and return consensus"""
        start_time = datetime.now()
        
        # Run analysis on all available models in parallel
        tasks = []
        for model_name, model_config in self.models.items():
            if model_config['client']:
                task = self._analyze_with_model(
                    model_name, 
                    model_config, 
                    resume_data, 
                    job_analysis
                )
                tasks.append(task)
        
        # Wait for all models to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions and create ModelResult objects
        model_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Model {list(self.models.keys())[i]} failed: {str(result)}")
                continue
            model_results.append(result)
        
        if not model_results:
            raise Exception("All AI models failed")
        
        # Create consensus analysis
        consensus = self._create_consensus_analysis(model_results, resume_data, job_analysis)
        
        processing_time = (datetime.now() - start_time).total_seconds()
        consensus['processing_time'] = processing_time
        consensus['models_used'] = [r.model_name for r in model_results]
        consensus['timestamp'] = datetime.now().isoformat()
        
        return consensus
    
    async def _analyze_with_model(self, model_name: str, model_config: Dict, 
                                resume_data: Dict, job_analysis: Dict) -> ModelResult:
        """Analyze resume with a specific model"""
        start_time = datetime.now()
        
        try:
            if model_name.startswith('gpt'):
                analysis = await self._analyze_with_openai(model_config, resume_data, job_analysis)
            elif model_name == 'claude':
                analysis = await self._analyze_with_claude(model_config, resume_data, job_analysis)
            elif model_name == 'gemini':
                analysis = await self._analyze_with_gemini(model_config, resume_data, job_analysis)
            else:
                raise Exception(f"Unknown model: {model_name}")
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return ModelResult(
                model_name=model_name,
                score=analysis.get('total_score', 0),
                confidence=analysis.get('confidence', 0.8),
                analysis=analysis,
                processing_time=processing_time,
                cost=analysis.get('cost', 0)
            )
            
        except Exception as e:
            logger.error(f"Error analyzing with {model_name}: {str(e)}")
            return ModelResult(
                model_name=model_name,
                score=0,
                confidence=0,
                analysis={},
                processing_time=0,
                cost=0,
                error=str(e)
            )
    
    async def _analyze_with_openai(self, model_config: Dict, resume_data: Dict, job_analysis: Dict) -> Dict:
        """Analyze with OpenAI models"""
        client = model_config['client']
        model = model_config['client'].models.list().data[0].id if hasattr(model_config['client'], 'models') else 'gpt-4-turbo'
        
        prompt = self._create_analysis_prompt(resume_data, job_analysis)
        
        messages = [
            {"role": "system", "content": "You are an expert ATS resume analyzer. Provide detailed analysis in JSON format."},
            {"role": "user", "content": prompt}
        ]
        
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=model_config['max_tokens'],
            temperature=model_config['temperature']
        )
        
        content = response.choices[0].message.content
        
        # Parse JSON response
        try:
            analysis = json.loads(content)
        except json.JSONDecodeError:
            # Fallback parsing
            analysis = self._parse_text_response(content)
        
        # Calculate cost (approximate)
        cost = self._calculate_openai_cost(response.usage.total_tokens, model)
        analysis['cost'] = cost
        
        return analysis
    
    async def _analyze_with_claude(self, model_config: Dict, resume_data: Dict, job_analysis: Dict) -> Dict:
        """Analyze with Claude models"""
        client = model_config['client']
        
        prompt = self._create_analysis_prompt(resume_data, job_analysis)
        
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=model_config['max_tokens'],
            temperature=model_config['temperature'],
            messages=[{"role": "user", "content": prompt}]
        )
        
        content = response.content[0].text
        
        try:
            analysis = json.loads(content)
        except json.JSONDecodeError:
            analysis = self._parse_text_response(content)
        
        # Calculate cost (approximate)
        cost = self._calculate_claude_cost(response.usage.input_tokens + response.usage.output_tokens)
        analysis['cost'] = cost
        
        return analysis
    
    async def _analyze_with_gemini(self, model_config: Dict, resume_data: Dict, job_analysis: Dict) -> Dict:
        """Analyze with Gemini models"""
        model = model_config['client']
        
        prompt = self._create_analysis_prompt(resume_data, job_analysis)
        
        response = model.generate_content(
            prompt,
            generation_config={
                'max_output_tokens': model_config['max_tokens'],
                'temperature': model_config['temperature']
            }
        )
        
        content = response.text
        
        try:
            analysis = json.loads(content)
        except json.JSONDecodeError:
            analysis = self._parse_text_response(content)
        
        # Calculate cost (approximate)
        cost = self._calculate_gemini_cost(len(prompt), len(content))
        analysis['cost'] = cost
        
        return analysis
    
    def _create_analysis_prompt(self, resume_data: Dict, job_analysis: Dict) -> str:
        """Create analysis prompt for AI models"""
        return f"""
        Analyze this resume for ATS compatibility and job match:

        RESUME DATA:
        {json.dumps(resume_data, indent=2)}

        JOB ANALYSIS:
        {json.dumps(job_analysis, indent=2)}

        Provide analysis in this JSON format:
        {{
            "total_score": 85,
            "confidence": 0.9,
            "component_scores": {{
                "keyword_match": 90,
                "skills_alignment": 85,
                "experience_relevance": 80,
                "format_compatibility": 95,
                "achievements_impact": 75,
                "completeness": 90
            }},
            "strengths": ["Strong technical skills", "Relevant experience"],
            "weaknesses": ["Missing keywords", "Weak achievements"],
            "improvements": ["Add more metrics", "Include industry keywords"],
            "ats_compatibility": 92,
            "job_match_percentage": 88,
            "recommendations": ["Optimize for ATS", "Add quantifiable achievements"]
        }}
        """
    
    def _parse_text_response(self, content: str) -> Dict:
        """Parse text response when JSON parsing fails"""
        # Extract score from text
        import re
        score_match = re.search(r'score[:\s]+(\d+)', content, re.IGNORECASE)
        score = int(score_match.group(1)) if score_match else 70
        
        return {
            'total_score': score,
            'confidence': 0.7,
            'component_scores': {
                'keyword_match': score - 5,
                'skills_alignment': score,
                'experience_relevance': score - 10,
                'format_compatibility': score + 5,
                'achievements_impact': score - 15,
                'completeness': score - 5
            },
            'strengths': ['AI analysis completed'],
            'weaknesses': ['JSON parsing failed'],
            'improvements': ['Manual review recommended'],
            'ats_compatibility': score,
            'job_match_percentage': score - 10,
            'recommendations': ['Review AI analysis results']
        }
    
    def _create_consensus_analysis(self, model_results: List[ModelResult], 
                                 resume_data: Dict, job_analysis: Dict) -> Dict[str, Any]:
        """Create consensus analysis from multiple model results"""
        if not model_results:
            raise Exception("No model results available")
        
        # Calculate weighted average scores
        total_weight = sum(self.model_weights.get(r.model_name, 0.1) for r in model_results)
        weighted_score = sum(
            r.score * self.model_weights.get(r.model_name, 0.1) 
            for r in model_results
        ) / total_weight
        
        # Calculate confidence as average of model confidences
        avg_confidence = sum(r.confidence for r in model_results) / len(model_results)
        
        # Aggregate component scores
        component_scores = {}
        for component in ['keyword_match', 'skills_alignment', 'experience_relevance', 
                         'format_compatibility', 'achievements_impact', 'completeness']:
            scores = [r.analysis.get('component_scores', {}).get(component, 0) for r in model_results]
            if scores:
                component_scores[component] = sum(scores) / len(scores)
            else:
                component_scores[component] = 0
        
        # Aggregate strengths, weaknesses, and improvements
        all_strengths = []
        all_weaknesses = []
        all_improvements = []
        
        for result in model_results:
            all_strengths.extend(result.analysis.get('strengths', []))
            all_weaknesses.extend(result.analysis.get('weaknesses', []))
            all_improvements.extend(result.analysis.get('improvements', []))
        
        # Remove duplicates and rank by frequency
        strengths = self._rank_by_frequency(all_strengths)
        weaknesses = self._rank_by_frequency(all_weaknesses)
        improvements = self._rank_by_frequency(all_improvements)
        
        # Calculate consensus grade
        grade = self._calculate_grade(weighted_score)
        
        return {
            'total_score': round(weighted_score, 2),
            'grade': grade,
            'confidence': round(avg_confidence, 2),
            'component_scores': {k: round(v, 2) for k, v in component_scores.items()},
            'strengths': strengths[:5],  # Top 5 strengths
            'weaknesses': weaknesses[:5],  # Top 5 weaknesses
            'improvements': improvements[:5],  # Top 5 improvements
            'ats_compatibility': round(weighted_score, 2),
            'job_match_percentage': round(weighted_score - 5, 2),
            'recommendations': improvements[:3],  # Top 3 recommendations
            'model_consensus': {
                'agreement_level': self._calculate_agreement(model_results),
                'model_scores': {r.model_name: r.score for r in model_results},
                'processing_times': {r.model_name: r.processing_time for r in model_results},
                'total_cost': sum(r.cost for r in model_results)
            }
        }
    
    def _rank_by_frequency(self, items: List[str]) -> List[str]:
        """Rank items by frequency of occurrence"""
        from collections import Counter
        counter = Counter(items)
        return [item for item, count in counter.most_common()]
    
    def _calculate_grade(self, score: float) -> str:
        """Calculate letter grade from score"""
        if score >= 90:
            return 'A+'
        elif score >= 85:
            return 'A'
        elif score >= 80:
            return 'A-'
        elif score >= 75:
            return 'B+'
        elif score >= 70:
            return 'B'
        elif score >= 65:
            return 'B-'
        elif score >= 60:
            return 'C+'
        elif score >= 55:
            return 'C'
        else:
            return 'D'
    
    def _calculate_agreement(self, model_results: List[ModelResult]) -> float:
        """Calculate agreement level between models"""
        if len(model_results) < 2:
            return 1.0
        
        scores = [r.score for r in model_results]
        mean_score = sum(scores) / len(scores)
        variance = sum((score - mean_score) ** 2 for score in scores) / len(scores)
        std_dev = variance ** 0.5
        
        # Agreement is higher when standard deviation is lower
        agreement = max(0, 1 - (std_dev / 50))  # Normalize by 50 points
        return round(agreement, 2)
    
    def _calculate_openai_cost(self, tokens: int, model: str) -> float:
        """Calculate OpenAI API cost"""
        if 'gpt-4' in model:
            return tokens * 0.00003  # Approximate cost per token
        else:
            return tokens * 0.000002
    
    def _calculate_claude_cost(self, tokens: int) -> float:
        """Calculate Claude API cost"""
        return tokens * 0.000015  # Approximate cost per token
    
    def _calculate_gemini_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Calculate Gemini API cost"""
        return (input_tokens * 0.0000005) + (output_tokens * 0.0000015)

# Example usage
if __name__ == "__main__":
    # Test the multi-model client
    client = MultiModelAIClient()
    
    # Sample resume data
    resume_data = {
        "contact": {"name": "John Doe", "email": "john@example.com"},
        "summary": "Experienced software developer",
        "experience": [{"title": "Software Engineer", "company": "Tech Corp"}],
        "skills": {"technical": ["Python", "JavaScript", "React"]}
    }
    
    job_analysis = {
        "required_skills": ["Python", "React", "AWS"],
        "tools_technologies": ["Docker", "Kubernetes"],
        "experience_years": 3
    }
    
    # Run analysis
    import asyncio
    result = asyncio.run(client.analyze_resume_multi_model(resume_data, job_analysis))
    print(json.dumps(result, indent=2))
