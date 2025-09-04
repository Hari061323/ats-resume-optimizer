# 🚀 AI-Powered ATS Resume Optimizer

A revolutionary AI-powered resume optimization system that uses advanced machine learning and natural language processing to help job seekers create ATS-friendly resumes that stand out to recruiters and hiring managers.

## ✨ Features

### 🤖 **Intelligent AI Analysis**
- **GPT-4 Powered Analysis**: Comprehensive 7-dimensional resume evaluation
- **Learning-Based Scoring**: Advanced project experience and skill assessment
- **Job Relevance Matching**: Smart alignment with job requirements
- **Industry Insights**: Market-specific recommendations and trends

### 📊 **Analytics Dashboard**
- **Real-time Tracking**: Monitor resume performance and improvements
- **Score Analytics**: Track progress over time with detailed metrics
- **User Insights**: Personalized recommendations and improvement areas
- **System Performance**: Monitor system health and usage statistics

### ✨ **Resume Enhancement**
- **4 Enhancement Levels**: From minimal to comprehensive improvements
- **Professional Formatting**: Clean, ATS-friendly document generation
- **Keyword Optimization**: Strategic keyword placement and density
- **Achievement Quantification**: Transform bullet points into impact statements

### 📄 **Document Generation**
- **Professional Templates**: Industry-standard resume formats
- **Download System**: Instant access to enhanced resumes
- **Format Preservation**: Maintains original document structure
- **Quality Assurance**: Automated formatting and style checks

## 🛠️ Technology Stack

- **Backend**: FastAPI (Python 3.13+)
- **AI Models**: OpenAI GPT-4, GPT-3.5-turbo
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Document Processing**: PyPDF2, python-docx
- **Analytics**: JSON-based data persistence
- **Server**: Uvicorn ASGI server

## 🚀 Quick Start

### Prerequisites
- Python 3.13 or higher
- OpenAI API key
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ats-resume-optimizer.git
   cd ats-resume-optimizer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp config.env .env
   # Edit .env and add your OpenAI API key
   ```

4. **Start the server**
   ```bash
   cd backend
   python fastapi_app.py
   ```

5. **Open the application**
   - Open `index.html` in your web browser
   - Or visit `http://localhost:8000` for API documentation

## 📋 API Endpoints

### Core Analysis
- `POST /analyze` - Traditional resume analysis
- `POST /enhance` - AI-powered resume enhancement
- `POST /intelligent-analysis` - GPT-4 comprehensive analysis

### Analytics
- `GET /analytics/system` - System-wide analytics
- `GET /analytics/dashboard/{user_id}` - User dashboard
- `GET /analytics/scores/{user_id}` - Score analytics
- `GET /analytics/performance` - Performance metrics

### Utilities
- `GET /health` - System health check
- `GET /jobs` - Sample job listings
- `GET /download/{filename}` - Download enhanced resumes

## 🎯 Usage

### 1. **Upload Resume**
- Support for PDF, DOCX, DOC, and TXT formats
- Maximum file size: 16MB
- Automatic text extraction and parsing

### 2. **Select Job**
- Choose from 15+ sample job descriptions
- Or provide custom job description
- Automatic keyword extraction and matching

### 3. **Run Analysis**
- **Traditional Analysis**: Quick ATS scoring
- **Intelligent Analysis**: Comprehensive GPT-4 evaluation
- **Resume Enhancement**: AI-powered improvements

### 4. **View Results**
- Detailed scoring breakdown
- Keyword matching analysis
- Improvement recommendations
- Download enhanced resume

## 📊 Performance Metrics

- **Response Time**: 50-60 seconds for intelligent analysis
- **Token Usage**: Optimized to 2,400-3,600 tokens per analysis
- **API Calls**: Reduced from 7 to 3 calls for faster processing
- **Success Rate**: 99%+ with comprehensive error handling

## 🔧 Configuration

### Environment Variables
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### File Limits
- Maximum file size: 16MB
- Supported formats: PDF, DOCX, DOC, TXT
- Upload directory: `backend/uploads/`

## 📁 Project Structure

```
ats-resume-optimizer/
├── backend/
│   ├── ai_*.py              # AI modules
│   ├── analytics_*.py       # Analytics system
│   ├── fastapi_app.py       # Main FastAPI application
│   └── docs/                # Documentation
├── index.html               # Frontend interface
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for providing the GPT-4 API
- FastAPI team for the excellent web framework
- The open-source community for various Python libraries

## 📞 Support

For support, email support@ats-resume-optimizer.com or create an issue in the GitHub repository.

---

**Built with ❤️ for job seekers worldwide**