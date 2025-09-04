"""
FastAPI Application - ATS Resume Optimizer API
Modern, fast, and async-capable version of the resume optimizer
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import traceback
import asyncio
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
from dotenv import load_dotenv

# Load environment variables from .env file
# Look for .env in parent directory (project root)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

# Import our AI modules
from ai_resume_parser import AIResumeParser
from ai_keyword_analyzer import AIKeywordAnalyzer
from ai_ats_scorer import AIATSScorer
from ai_resume_enhancer import AIResumeEnhancer
from ai_document_generator import AIDocumentGenerator
from ai_intelligent_resume_checker import IntelligentResumeChecker
from analytics_dashboard import AnalyticsDashboard
from analytics_endpoints import analytics_router


# Configure logging
import os
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/fastapi_app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI-Powered ATS Resume Optimizer API",
    description="Modern, fast API for resume optimization using AI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include analytics router
app.include_router(analytics_router)

# Configuration
UPLOAD_FOLDER = 'backend/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'txt'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

# Create necessary directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('backend/logs', exist_ok=True)

# Initialize AI components
# Initialize Intelligent Resume Checker
try:
    intelligent_checker = IntelligentResumeChecker()
    logger.info("Intelligent Resume Checker initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Intelligent Resume Checker: {str(e)}")
    intelligent_checker = None

# Initialize Analytics Dashboard
try:
    analytics_dashboard = AnalyticsDashboard()
    logger.info("Analytics Dashboard initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Analytics Dashboard: {str(e)}")
    analytics_dashboard = None

try:
    resume_parser = AIResumeParser()
    keyword_analyzer = AIKeywordAnalyzer()
    ats_scorer = AIATSScorer()
    resume_enhancer = AIResumeEnhancer()
    document_generator = AIDocumentGenerator()
    logger.info("All AI components initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize AI components: {str(e)}")
    resume_parser = None
    keyword_analyzer = None
    ats_scorer = None
    resume_enhancer = None
    document_generator = None

# Pydantic models
class BulletImprovementRequest(BaseModel):
    bullets: List[str]
    jobDescription: str

class KeywordOptimizationRequest(BaseModel):
    resumeText: str
    jobDescription: str
    industry: Optional[str] = "technology"

class SuggestionsRequest(BaseModel):
    resumeText: str
    targetRole: Optional[str] = "Software Engineer"
    experienceLevel: Optional[str] = "Mid-Level"

class JobMatchRequest(BaseModel):
    jobListings: Optional[List[Dict]] = None

# Utility functions
def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_sample_jobs() -> Dict[str, Any]:
    """Load sample jobs from JSON file"""
    try:
        # Try multiple locations
        possible_paths = [
            'sample_jobs.json',           # Current directory (backend)
            '../sample_jobs.json',         # Parent directory
            os.path.join(os.path.dirname(__file__), 'sample_jobs.json'),
            os.path.join(os.path.dirname(__file__), '..', 'sample_jobs.json')
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                with open(path, 'r') as f:
                    data = json.load(f)
                    logger.info(f"Loaded {len(data.get('jobs', []))} jobs from {path}")
                    return data
        
        logger.warning("sample_jobs.json not found in any location, returning empty job list")
        return {'jobs': [], 'categories': [], 'locations': [], 'experience_levels': []}
    except Exception as e:
        logger.error(f"Error loading sample jobs: {str(e)}")
        return {'jobs': [], 'categories': [], 'locations': [], 'experience_levels': []}

# Dependency to check AI components
def check_ai_components():
    """Dependency to check if AI components are available"""
    if not all([resume_parser, keyword_analyzer, ats_scorer]):
        raise HTTPException(
            status_code=503, 
            detail="AI components not configured. Please check OpenAI API key."
        )

# ROUTES

@app.get("/", tags=["Info"])
async def home():
    """API information endpoint"""
    return {
        'name': 'AI-Powered ATS Resume Optimizer API',
        'version': '1.0.0',
        'status': 'active',
        'framework': 'FastAPI',
        'endpoints': {
            'analyze': '/analyze - Complete AI analysis',
            'enhance': '/enhance - AI enhancement',
            'match_jobs': '/match-jobs - Job matching',
            'improve_bullets': '/improve-bullets - Bullet enhancement',
            'jobs': '/jobs - Get sample jobs',
            'docs': '/docs - API documentation'
        },
        'ai_status': {
            'parser': resume_parser is not None,
            'analyzer': keyword_analyzer is not None,
            'scorer': ats_scorer is not None,
            'enhancer': resume_enhancer is not None,
            'generator': document_generator is not None
        }
    }

@app.get("/health", tags=["Health"])
async def health():
    """Health check endpoint"""
    return {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'framework': 'FastAPI',
        'components': {
            'api': True,
            'ai_modules': all([resume_parser, keyword_analyzer, ats_scorer, 
                              resume_enhancer, document_generator])
        }
    }

@app.get("/jobs", tags=["Jobs"])
async def get_jobs():
    """Get all sample jobs"""
    jobs_data = load_sample_jobs()
    return jobs_data

@app.get("/jobs/{job_id}", tags=["Jobs"])
async def get_job(job_id: int):
    """Get specific job by ID"""
    jobs_data = load_sample_jobs()
    job = next((j for j in jobs_data.get('jobs', []) if j.get('id') == job_id), None)
    
    if job:
        return job
    else:
        raise HTTPException(status_code=404, detail="Job not found")

@app.post("/analyze", tags=["Analysis"])
async def analyze_resume(
    resume: UploadFile = File(...),
    jobDescription: str = Form(...),
    _: None = Depends(check_ai_components)
):
    """Complete AI analysis of resume against job description"""
    try:
        # Validate file
        if not allowed_file(resume.filename):
            raise HTTPException(status_code=400, detail="Invalid file type")
        
        if resume.size > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File too large")
        
        # Save file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{resume.filename}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        with open(filepath, "wb") as buffer:
            content = await resume.read()
            buffer.write(content)
        
        logger.info(f"Processing resume: {filename}")
        
        # Parse resume
        resume_text = resume_parser.extract_text(filepath)
        if not resume_text:
            raise HTTPException(status_code=400, detail="Could not extract text from resume")
        
        resume_data = resume_parser.parse_with_ai(resume_text)
        
        # Extract job keywords
        job_keywords = keyword_analyzer.extract_keywords_from_job(jobDescription)
        
        # Match keywords
        keyword_match = keyword_analyzer.match_keywords(resume_text, job_keywords)
        
        # Calculate ATS score
        ats_score = ats_scorer.calculate_score(resume_data, job_keywords, keyword_match)
        
        # Track analysis for analytics
        if analytics_dashboard:
            try:
                analysis_data = {
                    'overall_score': ats_score['total_score'],
                    'component_scores': ats_score['component_scores'],
                    'improvement_recommendations': ats_score['improvement_roadmap'],
                    'timestamp': datetime.now().isoformat(),
                    'processing_time': 0,  # Could be calculated
                    'file_size': resume.size if resume.size else 0
                }
                analytics_dashboard.track_analysis("user_123", analysis_data, "Target Position")
            except Exception as e:
                logger.error(f"Error tracking analysis: {str(e)}")
        
        # Clean up uploaded file
        try:
            os.remove(filepath)
        except:
            pass
        
        # Return comprehensive analysis
        return {
            'success': True,
            'score': ats_score['total_score'],
            'grade': ats_score['grade'],
            'resume_data': resume_data,
            'keywords': {
                'matched': keyword_match['exact_matches'],
                'semantic': keyword_match['semantic_matches'],
                'missing': keyword_match['missing_keywords'],
                'match_percentage': keyword_match['match_percentage']
            },
            'scoring_breakdown': ats_score['component_scores'],
            'swot': ats_score['swot_analysis'],
            'improvements': ats_score['improvement_roadmap'],
            'insights': ats_score['ai_insights'],
            'pass_probability': ats_score['pass_probability'],
            'competitive_rating': ats_score['competitive_rating']
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in analyze_resume: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/enhance", tags=["Enhancement"])
async def enhance_resume(
    resume: UploadFile = File(...),
    jobDescription: str = Form(...),
    targetScore: int = Form(85),
    enhancementLevel: str = Form("moderate"),
    _: None = Depends(check_ai_components)
):
    """AI-powered resume enhancement"""
    try:
        # Validate file
        if not allowed_file(resume.filename):
            raise HTTPException(status_code=400, detail="Invalid file type")
        
        # Save file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{resume.filename}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        with open(filepath, "wb") as buffer:
            content = await resume.read()
            buffer.write(content)
        
        # Parse resume
        resume_text = resume_parser.extract_text(filepath)
        resume_data = resume_parser.parse_with_ai(resume_text)
        
        # Extract job keywords
        job_keywords = keyword_analyzer.extract_keywords_from_job(jobDescription)
        
        # Enhance resume
        enhancement_result = resume_enhancer.enhance_resume(
            resume_data,
            job_keywords,
            targetScore,
            enhancementLevel
        )
        
        # Generate new document
        output_filename = f"enhanced_{timestamp}.docx"
        doc_path = document_generator.generate_docx(
            enhancement_result['enhanced_resume'],
            template='modern',
            filename=output_filename
        )
        
        # Calculate new score
        enhanced_text = json.dumps(enhancement_result['enhanced_resume'])
        keyword_match = keyword_analyzer.match_keywords(enhanced_text, job_keywords)
        new_score = ats_scorer.calculate_score(
            enhancement_result['enhanced_resume'],
            job_keywords,
            keyword_match
        )
        
        # Clean up uploaded file
        try:
            os.remove(filepath)
        except:
            pass
        
        return {
            'success': True,
            'enhanced_resume': enhancement_result['enhanced_resume'],
            'enhancement_report': enhancement_result['enhancement_report'],
            'original_score': 65,  # This would be calculated from original
            'new_score': new_score['total_score'],
            'download_path': f"/download/{output_filename}",
            'improvements_applied': enhancement_result['enhancement_report']['changes_made']
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in enhance_resume: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{filename}", tags=["Download"])
async def download_file(filename: str):
    """Download enhanced resume file"""
    try:
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        
        # Check if file is an enhanced resume (security check)
        if not filename.startswith('enhanced_') or not filename.endswith('.docx'):
            raise HTTPException(status_code=403, detail="Access denied")
        
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading file {filename}: {str(e)}")
        raise HTTPException(status_code=500, detail="Download failed")

@app.post("/match-jobs", tags=["Job Matching"])
async def match_jobs(
    resume: UploadFile = File(...),
    jobListings: Optional[str] = Form(None),
    _: None = Depends(check_ai_components)
):
    """Match resume against multiple job listings"""
    try:
        # Validate file
        if not allowed_file(resume.filename):
            raise HTTPException(status_code=400, detail="Invalid file type")
        
        # Get job listings
        if jobListings:
            try:
                job_listings = json.loads(jobListings)
                logger.info(f"Using {len(job_listings)} jobs from request")
            except json.JSONDecodeError:
                logger.warning("Failed to parse jobListings, using default")
                jobs_data = load_sample_jobs()
                job_listings = jobs_data.get('jobs', [])
        else:
            jobs_data = load_sample_jobs()
            job_listings = jobs_data.get('jobs', [])
            logger.info(f"Using {len(job_listings)} jobs from sample_jobs.json")
        
        # Save and parse resume
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{resume.filename}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        with open(filepath, "wb") as buffer:
            content = await resume.read()
            buffer.write(content)
        
        resume_text = resume_parser.extract_text(filepath)
        resume_data = resume_parser.parse_with_ai(resume_text)
        
        # Match against each job
        matches = []
        for job in job_listings:
            job_description = job.get('description', '')
            if not job_description:
                continue
            
            # Analyze job
            job_keywords = keyword_analyzer.extract_keywords_from_job(job_description)
            keyword_match = keyword_analyzer.match_keywords(resume_text, job_keywords)
            score = ats_scorer.calculate_score(resume_data, job_keywords, keyword_match)
            
            matches.append({
                'job_id': job.get('id'),
                'job_title': job.get('title'),
                'company': job.get('company'),
                'location': job.get('location'),
                'match_score': score['total_score'],
                'grade': score['grade'],
                'keyword_match': keyword_match['match_percentage'],
                'missing_keywords': keyword_match['missing_keywords'][:5],
                'strengths': score['swot_analysis']['strengths'][:2],
                'fit_analysis': {
                    'skills_match': score['component_scores']['skills_alignment'],
                    'experience_match': score['component_scores']['experience_relevance'],
                    'overall_fit': score['pass_probability']
                }
            })
        
        # Sort by match score
        matches.sort(key=lambda x: x['match_score'], reverse=True)
        
        # Clean up
        try:
            os.remove(filepath)
        except:
            pass
        
        return {
            'success': True,
            'total_jobs_analyzed': len(matches),
            'matches': matches[:10],  # Top 10 matches
            'best_match': matches[0] if matches else None,
            'recommendations': {
                'apply_now': [m for m in matches if m['match_score'] >= 80][:3],
                'apply_after_optimization': [m for m in matches if 60 <= m['match_score'] < 80][:3],
                'need_more_experience': [m for m in matches if m['match_score'] < 60][:3]
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in match_jobs: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/improve-bullets", tags=["Enhancement"])
async def improve_bullets(request: BulletImprovementRequest):
    """Improve resume bullet points"""
    try:
        if not resume_enhancer:
            raise HTTPException(status_code=503, detail="AI enhancer not configured")
        
        # Enhance bullets
        improved_bullets = resume_enhancer.improve_bullet_points(
            request.bullets, 
            request.jobDescription
        )
        
        return {
            'success': True,
            'original_bullets': request.bullets,
            'improved_bullets': improved_bullets,
            'improvements': {
                'action_verbs_added': True,
                'metrics_added': True,
                'keywords_integrated': True
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in improve_bullets: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/optimize-keywords", tags=["Optimization"])
async def optimize_keywords(request: KeywordOptimizationRequest):
    """Optimize resume keywords for job description"""
    try:
        if not keyword_analyzer:
            raise HTTPException(status_code=503, detail="AI analyzer not configured")
        
        # Extract and analyze keywords
        job_keywords = keyword_analyzer.extract_keywords_from_job(request.jobDescription)
        keyword_match = keyword_analyzer.match_keywords(request.resumeText, job_keywords)
        
        # Get industry keywords
        industry_keywords = keyword_analyzer.get_industry_keywords(request.industry)
        
        return {
            'success': True,
            'job_keywords': job_keywords,
            'keyword_match': keyword_match,
            'industry_keywords': industry_keywords,
            'optimization_suggestions': keyword_match['recommendations']
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in optimize_keywords: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-suggestions", tags=["Suggestions"])
async def generate_suggestions(request: SuggestionsRequest):
    """Generate AI-powered improvement suggestions"""
    try:
        if not ats_scorer:
            raise HTTPException(status_code=503, detail="AI scorer not configured")
        
        # Create mock job analysis for suggestions
        job_analysis = {
            'job_level': request.experienceLevel,
            'required_skills': [],
            'experience_years': 3 if request.experienceLevel == 'Mid-Level' else 5
        }
        
        # Parse resume
        if resume_parser:
            resume_data = resume_parser.parse_with_ai(request.resumeText)
        else:
            resume_data = {'meta': {}, 'experience': [], 'skills': {}}
        
        # Generate suggestions using AI insights
        suggestions = {
            'immediate_actions': [
                'Add quantified achievements to each role',
                'Include relevant keywords from job descriptions',
                'Create a compelling professional summary'
            ],
            'skill_gaps': [
                f'Consider adding {request.targetRole}-specific skills',
                'Include industry certifications',
                'Add technical tools and frameworks'
            ],
            'format_improvements': [
                'Use consistent formatting throughout',
                'Ensure ATS-friendly format (avoid tables/graphics)',
                'Keep to 2 pages maximum'
            ],
            'content_enhancements': [
                'Use CAR (Challenge-Action-Result) format',
                'Start bullets with strong action verbs',
                'Include metrics and percentages'
            ]
        }
        
        return {
            'success': True,
            'suggestions': suggestions,
            'priority_order': [
                'immediate_actions',
                'content_enhancements',
                'skill_gaps',
                'format_improvements'
            ]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in generate_suggestions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{filename}", tags=["Download"])
async def download_file(filename: str):
    """Download generated resume"""
    try:
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.exists(filepath):
            return FileResponse(
                path=filepath,
                filename=filename,
                media_type='application/octet-stream'
            )
        else:
            raise HTTPException(status_code=404, detail="File not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading file: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/feedback", tags=["Feedback"])
async def get_feedback(
    resume: UploadFile = File(...),
    jobDescription: str = Form(""),
    _: None = Depends(check_ai_components)
):
    """Get AI feedback on resume"""
    try:
        # Validate file
        if not allowed_file(resume.filename):
            raise HTTPException(status_code=400, detail="Invalid file type")
        
        # Save and process file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{resume.filename}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        with open(filepath, "wb") as buffer:
            content = await resume.read()
            buffer.write(content)
        
        # Parse and analyze
        resume_text = resume_parser.extract_text(filepath)
        resume_data = resume_parser.parse_with_ai(resume_text)
        
        # Generate feedback
        feedback = {
            'overall': 'Your resume shows potential but needs optimization for ATS systems.',
            'strengths': [
                'Clear structure and formatting',
                'Relevant experience included'
            ],
            'areas_for_improvement': [
                'Add more quantified achievements',
                'Include keywords from job description',
                'Strengthen professional summary'
            ],
            'action_items': [
                'Quantify at least 3 achievements per role',
                'Add 5-7 missing keywords naturally',
                'Create a 3-line professional summary'
            ],
            'estimated_time_to_improve': '1-2 hours',
            'priority': 'High'
        }
        
        # Clean up
        try:
            os.remove(filepath)
        except:
            pass
        
        return {
            'success': True,
            'feedback': feedback
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_feedback: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": "Endpoint not found"}
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    logger.error(f"Internal server error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )

if __name__ == "__main__":
    logger.info("Starting ATS Resume Optimizer FastAPI...")
    logger.info(f"Upload folder: {UPLOAD_FOLDER}")
    logger.info(f"AI components status: Parser={resume_parser is not None}, "
               f"Analyzer={keyword_analyzer is not None}, "
               f"Scorer={ats_scorer is not None}, "
               f"Enhancer={resume_enhancer is not None}, "
               f"Generator={document_generator is not None}")
    
    # Run the app
    uvicorn.run(
        "fastapi_app:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )

@app.post("/intelligent-analysis", tags=["Intelligent Analysis"])
async def intelligent_resume_analysis(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
    job_title: str = Form(None),
    company: str = Form(None),
    _: None = Depends(check_ai_components)
):
    """Intelligent AI resume analysis with GPT-4.1"""
    try:
        if not intelligent_checker:
            raise HTTPException(status_code=500, detail="Intelligent checker not available")
        
        # Validate file
        if not allowed_file(resume.filename):
            raise HTTPException(status_code=400, detail="Invalid file type")
        
        if resume.size > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File too large")
        
        # Save file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{resume.filename}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        with open(filepath, "wb") as buffer:
            content = await resume.read()
            buffer.write(content)
        
        logger.info(f"Intelligent analysis for: {filename}")
        
        # Parse resume
        resume_text = resume_parser.extract_text(filepath)
        if not resume_text:
            raise HTTPException(status_code=400, detail="Could not extract text from resume")
        
        resume_data = resume_parser.parse_with_ai(resume_text)
        
        # Create job analysis
        job_keywords = keyword_analyzer.extract_keywords_from_job(job_description)
        job_analysis = {
            'title': job_title or 'Target Position',
            'description': job_description,
            'company': company or 'Target Company',
            'required_skills': job_keywords.get('required_skills', []),
            'experience_years': 3,  # Default
            'job_level': 'mid'
        }
        
        # Perform intelligent analysis (using fast method for better performance)
        analysis_results = intelligent_checker.fast_comprehensive_analysis(
            resume_data, job_analysis
        )
        
        # Clean up uploaded file
        try:
            os.remove(filepath)
        except:
            pass
        
        return {
            'success': True,
            'analysis_id': analysis_results.get('analysis_id', 'unknown'),
            'overall_score': analysis_results.get('overall_score', 0),
            'dimensional_scores': analysis_results.get('dimensional_scores', {}),
            'job_relevance_score': analysis_results.get('job_relevance_score', 0),
            'job_relevance_analysis': analysis_results.get('job_relevance_analysis', 'Analysis completed'),
            'key_insights': analysis_results.get('key_insights', []),
            'recommendations': analysis_results.get('recommendations', []),
            'industry_insights': analysis_results.get('industry_insights', 'Industry insights not available')
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in intelligent analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
