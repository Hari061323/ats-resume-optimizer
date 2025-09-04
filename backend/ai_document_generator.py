"""
AI Document Generator
Generates formatted DOCX resumes from enhanced data
"""

import os
from typing import Dict, Any
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.style import WD_STYLE_TYPE
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
# Look for .env in parent directory (project root)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AIDocumentGenerator:
    """Generate professional DOCX resumes"""
    
    def __init__(self):
        self.templates = {
            'modern': {
                'font': 'Calibri',
                'heading_size': 16,
                'subheading_size': 12,
                'body_size': 11,
                'color': RGBColor(0, 0, 139)  # Dark blue
            },
            'classic': {
                'font': 'Times New Roman',
                'heading_size': 14,
                'subheading_size': 12,
                'body_size': 11,
                'color': RGBColor(0, 0, 0)  # Black
            },
            'executive': {
                'font': 'Georgia',
                'heading_size': 15,
                'subheading_size': 12,
                'body_size': 11,
                'color': RGBColor(25, 25, 112)  # Midnight blue
            }
        }
    
    def generate_docx(self, resume_data: Dict, template: str = 'modern', 
                     filename: str = None) -> str:
        """Generate DOCX resume from data"""
        
        # Create document
        doc = Document()
        
        # Apply template settings
        template_config = self.templates.get(template, self.templates['modern'])
        
        # Set document margins
        sections = doc.sections
        for section in sections:
            section.top_margin = Inches(0.5)
            section.bottom_margin = Inches(0.5)
            section.left_margin = Inches(0.7)
            section.right_margin = Inches(0.7)
        
        # Add content
        self._add_header(doc, resume_data.get('contact', {}), template_config)
        self._add_summary(doc, resume_data.get('summary', ''), template_config)
        self._add_experience(doc, resume_data.get('experience', []), template_config)
        self._add_education(doc, resume_data.get('education', []), template_config)
        self._add_skills(doc, resume_data.get('skills', {}), template_config)
        self._add_projects(doc, resume_data.get('projects', []), template_config)
        self._add_certifications(doc, resume_data.get('certifications', []), template_config)
        
        # Save document
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'enhanced_resume_{timestamp}.docx'
        
        filepath = os.path.join('backend', 'uploads', filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        doc.save(filepath)
        
        logger.info(f"Resume generated: {filepath}")
        return filepath
    
    def _add_header(self, doc: Document, contact: Dict, config: Dict):
        """Add contact header"""
        
        # Name
        name_para = doc.add_paragraph()
        name_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        name_run = name_para.add_run(contact.get('name', 'Your Name'))
        name_run.font.size = Pt(20)
        name_run.font.name = config['font']
        name_run.font.bold = True
        name_run.font.color.rgb = config['color']
        
        # Contact line
        contact_parts = []
        if contact.get('email'):
            contact_parts.append(contact['email'])
        if contact.get('phone'):
            contact_parts.append(contact['phone'])
        if contact.get('location'):
            contact_parts.append(contact['location'])
        
        if contact_parts:
            contact_para = doc.add_paragraph()
            contact_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            contact_run = contact_para.add_run(' | '.join(contact_parts))
            contact_run.font.size = Pt(10)
            contact_run.font.name = config['font']
        
        # LinkedIn/GitHub
        links = []
        if contact.get('linkedin'):
            links.append(f"LinkedIn: {contact['linkedin']}")
        if contact.get('github'):
            links.append(f"GitHub: {contact['github']}")
        if contact.get('portfolio'):
            links.append(f"Portfolio: {contact['portfolio']}")
        
        if links:
            links_para = doc.add_paragraph()
            links_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            links_run = links_para.add_run(' | '.join(links))
            links_run.font.size = Pt(10)
            links_run.font.name = config['font']
        
        # Add line break
        doc.add_paragraph()
    
    def _add_summary(self, doc: Document, summary: str, config: Dict):
        """Add professional summary"""
        
        if not summary:
            return
        
        # Section heading
        heading = doc.add_paragraph('PROFESSIONAL SUMMARY')
        self._format_heading(heading, config)
        
        # Summary text
        summary_para = doc.add_paragraph(summary)
        summary_para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        for run in summary_para.runs:
            run.font.size = Pt(config['body_size'])
            run.font.name = config['font']
        
        doc.add_paragraph()  # Space after section
    
    def _add_experience(self, doc: Document, experience: list, config: Dict):
        """Add experience section"""
        
        if not experience:
            return
        
        # Section heading
        heading = doc.add_paragraph('PROFESSIONAL EXPERIENCE')
        self._format_heading(heading, config)
        
        for exp in experience:
            # Job title and company
            title_para = doc.add_paragraph()
            title_run = title_para.add_run(exp.get('title', 'Position'))
            title_run.font.size = Pt(config['subheading_size'])
            title_run.font.name = config['font']
            title_run.font.bold = True
            
            title_para.add_run(' | ')
            company_run = title_para.add_run(exp.get('company', 'Company'))
            company_run.font.size = Pt(config['subheading_size'])
            company_run.font.name = config['font']
            
            # Location and duration
            details_para = doc.add_paragraph()
            details_text = []
            if exp.get('location'):
                details_text.append(exp['location'])
            if exp.get('duration'):
                details_text.append(exp['duration'])
            
            details_run = details_para.add_run(' | '.join(details_text))
            details_run.font.size = Pt(config['body_size'] - 1)
            details_run.font.name = config['font']
            details_run.font.italic = True
            
            # Responsibilities and achievements
            bullets = []
            bullets.extend(exp.get('responsibilities', []))
            bullets.extend(exp.get('achievements', []))
            bullets.extend(exp.get('metrics', []))
            
            for bullet in bullets:
                # Ensure bullet is a string
                if isinstance(bullet, list):
                    bullet = ' '.join(str(item) for item in bullet)
                elif not isinstance(bullet, str):
                    bullet = str(bullet)
                
                bullet_para = doc.add_paragraph(style='List Bullet')
                bullet_para.add_run(bullet).font.size = Pt(config['body_size'])
                bullet_para.paragraph_format.left_indent = Inches(0.25)
                bullet_para.paragraph_format.space_after = Pt(2)
                
                # Format font
                for run in bullet_para.runs:
                    run.font.name = config['font']
            
            doc.add_paragraph()  # Space between jobs
        
        doc.add_paragraph()  # Space after section
    
    def _add_education(self, doc: Document, education: list, config: Dict):
        """Add education section"""
        
        if not education:
            return
        
        # Section heading
        heading = doc.add_paragraph('EDUCATION')
        self._format_heading(heading, config)
        
        for edu in education:
            # Degree and field
            edu_para = doc.add_paragraph()
            degree_text = f"{edu.get('degree', 'Degree')} in {edu.get('field', 'Field')}"
            degree_run = edu_para.add_run(degree_text)
            degree_run.font.size = Pt(config['subheading_size'])
            degree_run.font.name = config['font']
            degree_run.font.bold = True
            
            # Institution and year
            details_para = doc.add_paragraph()
            institution = edu.get('institution', 'University')
            year = edu.get('year', '')
            gpa = edu.get('gpa', '')
            
            details_text = institution
            if year:
                details_text += f" | {year}"
            if gpa:
                details_text += f" | GPA: {gpa}"
            
            details_run = details_para.add_run(details_text)
            details_run.font.size = Pt(config['body_size'])
            details_run.font.name = config['font']
            
            doc.add_paragraph()  # Space between entries
        
        doc.add_paragraph()  # Space after section
    
    def _add_skills(self, doc: Document, skills: Dict, config: Dict):
        """Add skills section"""
        
        if not skills:
            return
        
        # Section heading
        heading = doc.add_paragraph('SKILLS')
        self._format_heading(heading, config)
        
        # Format skills by category
        skill_categories = [
            ('Technical Skills', skills.get('technical', [])),
            ('Programming Languages', skills.get('languages', [])),
            ('Tools & Technologies', skills.get('tools', [])),
            ('Frameworks', skills.get('frameworks', [])),
            ('Soft Skills', skills.get('soft', []))
        ]
        
        for category_name, skill_list in skill_categories:
            if skill_list:
                skill_para = doc.add_paragraph()
                
                # Category label
                category_run = skill_para.add_run(f"{category_name}: ")
                category_run.font.size = Pt(config['body_size'])
                category_run.font.name = config['font']
                category_run.font.bold = True
                
                # Skills
                skills_run = skill_para.add_run(', '.join(skill_list))
                skills_run.font.size = Pt(config['body_size'])
                skills_run.font.name = config['font']
        
        doc.add_paragraph()  # Space after section
    
    def _add_projects(self, doc: Document, projects: list, config: Dict):
        """Add projects section"""
        
        if not projects:
            return
        
        # Section heading
        heading = doc.add_paragraph('PROJECTS')
        self._format_heading(heading, config)
        
        for project in projects:
            # Project name
            name_para = doc.add_paragraph()
            name_run = name_para.add_run(project.get('name', 'Project'))
            name_run.font.size = Pt(config['subheading_size'])
            name_run.font.name = config['font']
            name_run.font.bold = True
            
            # Technologies
            if project.get('technologies'):
                tech_para = doc.add_paragraph()
                tech_run = tech_para.add_run(f"Technologies: {', '.join(project['technologies'])}")
                tech_run.font.size = Pt(config['body_size'] - 1)
                tech_run.font.name = config['font']
                tech_run.font.italic = True
            
            # Description
            if project.get('description'):
                desc_para = doc.add_paragraph(project['description'])
                for run in desc_para.runs:
                    run.font.size = Pt(config['body_size'])
                    run.font.name = config['font']
            
            # Achievements
            for achievement in project.get('achievements', []):
                bullet_para = doc.add_paragraph(style='List Bullet')
                bullet_para.add_run(achievement).font.size = Pt(config['body_size'])
                bullet_para.paragraph_format.left_indent = Inches(0.25)
                
                for run in bullet_para.runs:
                    run.font.name = config['font']
            
            doc.add_paragraph()  # Space between projects
        
        doc.add_paragraph()  # Space after section
    
    def _add_certifications(self, doc: Document, certifications: list, config: Dict):
        """Add certifications section"""
        
        if not certifications:
            return
        
        # Section heading
        heading = doc.add_paragraph('CERTIFICATIONS')
        self._format_heading(heading, config)
        
        for cert in certifications:
            cert_para = doc.add_paragraph()
            
            # Certification name
            cert_run = cert_para.add_run(cert.get('name', 'Certification'))
            cert_run.font.size = Pt(config['body_size'])
            cert_run.font.name = config['font']
            cert_run.font.bold = True
            
            # Issuer and date
            if cert.get('issuer'):
                cert_para.add_run(f" | {cert['issuer']}")
            if cert.get('date'):
                cert_para.add_run(f" | {cert['date']}")
            
            for run in cert_para.runs[1:]:  # Skip the first run (already formatted)
                run.font.size = Pt(config['body_size'])
                run.font.name = config['font']
        
        doc.add_paragraph()  # Space after section
    
    def _format_heading(self, paragraph, config: Dict):
        """Format section heading"""
        
        paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
        
        for run in paragraph.runs:
            run.font.size = Pt(config['heading_size'])
            run.font.name = config['font']
            run.font.bold = True
            run.font.color.rgb = config['color']
        
        # Add underline effect with paragraph border
        paragraph.paragraph_format.space_after = Pt(6)
        paragraph.paragraph_format.space_before = Pt(6)
    
    def generate_pdf(self, docx_path: str) -> str:
        """Convert DOCX to PDF (requires additional library)"""
        
        # Note: This would require python-docx2pdf or similar
        # For now, returning the DOCX path
        logger.info("PDF generation requires additional libraries. Returning DOCX.")
        return docx_path