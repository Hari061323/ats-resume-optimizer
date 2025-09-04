"""
AI-Powered Resume Parser
Extracts and structures resume content using GPT
"""

import json
import re
import requests
import os
from typing import Dict, Any, List, Optional
import PyPDF2
from docx import Document
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


class AIResumeParser:
    """AI-powered resume parser using GPT"""
    
    def __init__(self):
        self.client = OpenAIClient()
    
    def extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file"""
        try:
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
            return text
        except Exception as e:
            logger.error(f"Error extracting PDF text: {str(e)}")
            return ""
    
    def extract_text_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX file"""
        try:
            doc = Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
            return text
        except Exception as e:
            logger.error(f"Error extracting DOCX text: {str(e)}")
            return ""
    
    def extract_text(self, file_path: str) -> str:
        """Extract text from file based on extension"""
        file_ext = file_path.lower().split('.')[-1]
        
        if file_ext == 'pdf':
            return self.extract_text_from_pdf(file_path)
        elif file_ext in ['docx', 'doc']:
            return self.extract_text_from_docx(file_path)
        else:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
    
    def parse_with_ai(self, resume_text: str) -> Dict[str, Any]:
        """Use GPT to parse and structure resume content"""
        
        prompt = """Analyze this resume and extract the following information in JSON format:
        {
            "contact": {
                "name": "",
                "email": "",
                "phone": "",
                "location": "",
                "linkedin": "",
                "github": "",
                "portfolio": ""
            },
            "summary": "",
            "experience": [
                {
                    "title": "",
                    "company": "",
                    "location": "",
                    "duration": "",
                    "responsibilities": [],
                    "achievements": [],
                    "metrics": []
                }
            ],
            "education": [
                {
                    "degree": "",
                    "field": "",
                    "institution": "",
                    "year": "",
                    "gpa": ""
                }
            ],
            "skills": {
                "technical": [],
                "soft": [],
                "languages": [],
                "tools": [],
                "frameworks": []
            },
            "projects": [
                {
                    "name": "",
                    "description": "",
                    "technologies": [],
                    "achievements": []
                }
            ],
            "certifications": [
                {
                    "name": "",
                    "issuer": "",
                    "date": ""
                }
            ],
            "awards": [],
            "publications": [],
            "volunteer": []
        }
        
        Extract all relevant information. If a field is not found, use empty string or empty array.
        Focus on identifying:
        - Quantified achievements (percentages, dollar amounts, time saved)
        - Action verbs in experience descriptions
        - Technical and soft skills
        - Relevant keywords for ATS systems"""
        
        messages = [
            {"role": "system", "content": "You are an expert resume parser. Extract structured information from resumes accurately."},
            {"role": "user", "content": f"{prompt}\n\nResume:\n{resume_text}"}
        ]
        
        try:
            response = self.client.chat_completion(messages, temperature=0.3)
            content = response['choices'][0]['message']['content']
            
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                parsed_data = json.loads(json_match.group())
            else:
                parsed_data = json.loads(content)
            
            return self._enhance_parsed_data(parsed_data)
            
        except Exception as e:
            logger.error(f"Error parsing with AI: {str(e)}")
            return self._get_default_structure()
    
    def _enhance_parsed_data(self, data: Dict) -> Dict:
        """Enhance parsed data with additional analysis"""
        
        # Calculate experience years
        total_years = 0
        for exp in data.get('experience', []):
            duration = exp.get('duration', '')
            years_match = re.search(r'(\d+)\s*year', duration, re.IGNORECASE)
            if years_match:
                total_years += int(years_match.group(1))
        
        data['meta'] = {
            'total_experience_years': total_years,
            'skill_count': len(data.get('skills', {}).get('technical', [])) + 
                          len(data.get('skills', {}).get('soft', [])),
            'has_summary': bool(data.get('summary')),
            'has_quantified_achievements': self._has_metrics(data),
            'project_count': len(data.get('projects', [])),
            'certification_count': len(data.get('certifications', []))
        }
        
        return data
    
    def _has_metrics(self, data: Dict) -> bool:
        """Check if resume has quantified achievements"""
        metric_patterns = [r'\d+%', r'\$\d+', r'\d+\s*(hours?|days?|weeks?|months?)', 
                          r'\d+x', r'\d+\+']
        
        for exp in data.get('experience', []):
            for achievement in exp.get('achievements', []):
                for pattern in metric_patterns:
                    if re.search(pattern, achievement):
                        return True
        return False
    
    def _get_default_structure(self) -> Dict:
        """Return default resume structure"""
        return {
            "contact": {},
            "summary": "",
            "experience": [],
            "education": [],
            "skills": {
                "technical": [],
                "soft": [],
                "languages": [],
                "tools": [],
                "frameworks": []
            },
            "projects": [],
            "certifications": [],
            "awards": [],
            "publications": [],
            "volunteer": [],
            "meta": {
                "total_experience_years": 0,
                "skill_count": 0,
                "has_summary": False,
                "has_quantified_achievements": False,
                "project_count": 0,
                "certification_count": 0
            }
        }
    
    def extract_key_phrases(self, resume_data: Dict) -> List[str]:
        """Extract key phrases from parsed resume"""
        key_phrases = []
        
        # Extract from summary
        if resume_data.get('summary'):
            words = resume_data['summary'].split()
            key_phrases.extend([' '.join(words[i:i+3]) for i in range(len(words)-2)])
        
        # Extract from experience
        for exp in resume_data.get('experience', []):
            if exp.get('title'):
                key_phrases.append(exp['title'])
            for resp in exp.get('responsibilities', []):
                if len(resp.split()) > 3:
                    key_phrases.append(resp[:50])
        
        # Extract skills
        for skill_type in resume_data.get('skills', {}).values():
            if isinstance(skill_type, list):
                key_phrases.extend(skill_type)
        
        return list(set(key_phrases))[:50]  # Return top 50 unique phrases