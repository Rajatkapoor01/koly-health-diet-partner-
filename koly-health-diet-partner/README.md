# KOYL AI - Personalized Diet Recommendation System

KOYL AI is a full-stack AI-powered diet recommendation web application that provides personalized nutrition plans based on health symptoms and food allergies.

## 🏗️ Architecture

### Frontend (Next.js + React)
- Modern React interface with TypeScript
- Responsive design with Tailwind CSS
- Real-time form validation and user feedback
- Professional UI components with shadcn/ui

### Backend (Python + Flask)
- **RAG Pipeline**: Retrieval Augmented Generation with FAISS vector search
- **AI Models**: 
  - Sentence-BERT (all-MiniLM-L6-v2) for semantic retrieval
  - T5-small for text summarization and generation
- **Knowledge Base**: Curated data from PubMed, USDA, EatRight.org, Harvard Nutrition
- **Allergy Filtering**: Intelligent filtering system for food safety

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.8+
- 4GB+ RAM (for AI models)

### 1. Setup Backend
\`\`\`bash
# Install Python dependencies and setup environment
npm run setup-backend
\`\`\`

### 2. Setup Frontend
\`\`\`bash
# Install Node.js dependencies
npm install
\`\`\`

### 3. Configure Environment
\`\`\`bash
# Copy environment template
cp .env.example .env.local

# Edit environment variables
FLASK_BACKEND_URL=http://localhost:5000
\`\`\`

### 4. Start Full Stack
\`\`\`bash
# Start both frontend and backend
npm run start-fullstack
\`\`\`

The application will be available at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **Health Check**: http://localhost:5000/health

## 🔧 Manual Setup

### Backend Only
\`\`\`bash
# Activate virtual environment
source koyl_ai_env/bin/activate

# Start Flask server
npm run start-backend
\`\`\`

### Frontend Only
\`\`\`bash
# Start Next.js development server
npm run dev
\`\`\`

## 📡 API Endpoints

### POST /recommend
Generate personalized dietary recommendations.

**Request:**
\`\`\`json
{
  "symptoms": "I have high blood pressure and diabetes",
  "allergies": ["dairy", "gluten"],
  "user_profile": {
    "previous_recommendations": 0
  }
}
\`\`\`

**Response:**
\`\`\`json
{
  "recommendation": "# Personalized Dietary Recommendations...",
  "sources": [
    {
      "title": "Anti-inflammatory Diet Research",
      "url": "https://pubmed.ncbi.nlm.nih.gov/...",
      "type": "pubmed"
    }
  ],
  "allergy_masked": ["Dairy products [Removed - Allergy: dairy]"],
  "nutritional_highlights": ["Rich in omega-3 fatty acids"],
  "safety_score": 95,
  "confidence": 87
}
\`\`\`

### GET /health
Check backend system health.

## 🧠 AI Pipeline

### 1. Knowledge Retrieval
- User symptoms are encoded using Sentence-BERT
- FAISS performs semantic search across medical literature
- Top-k relevant documents are retrieved

### 2. Content Generation
- T5-small model generates personalized recommendations
- Context from retrieved documents guides generation
- Medical terminology and structure are maintained

### 3. Allergy Filtering
- Intelligent parsing of food allergies
- Automatic removal of allergenic foods
- Safe alternative suggestions provided

### 4. Quality Assurance
- Safety scoring based on allergy filtering
- Confidence scoring from retrieval quality
- Source attribution for transparency

## 🛡️ Safety Features

- **Allergy Protection**: Automatic filtering of allergenic foods
- **Medical Disclaimers**: Clear guidance to consult healthcare providers
- **Source Attribution**: All recommendations backed by research
- **Input Validation**: Comprehensive request validation
- **Error Handling**: Graceful fallbacks and error messages

## 🏥 Knowledge Sources

- **PubMed**: Peer-reviewed medical research
- **USDA**: Official nutritional composition data
- **EatRight.org**: Academy of Nutrition and Dietetics guidelines
- **Harvard T.H. Chan**: Public health and nutrition research

## 🔒 Privacy & Security

- No permanent data storage
- Session-based processing only
- CORS protection enabled
- Input sanitization and validation
- Medical disclaimer compliance

## 🚀 Deployment

### Production Environment
\`\`\`bash
# Build frontend
npm run build

# Start production servers
npm run start
\`\`\`

### Docker Deployment
\`\`\`dockerfile
# Dockerfile example for backend
FROM python:3.9-slim
WORKDIR /app
COPY scripts/backend/requirements.txt .
RUN pip install -r requirements.txt
COPY scripts/backend/ .
CMD ["python", "run_backend.py"]
\`\`\`

## 🧪 Testing

### Backend Health Check
\`\`\`bash
curl http://localhost:5000/health
\`\`\`

### Frontend API Test
\`\`\`bash
curl -X POST http://localhost:3000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{"symptoms":"fatigue","allergies":[]}'
\`\`\`

## 📊 Performance

- **Response Time**: < 3 seconds for recommendations
- **Memory Usage**: ~2GB for AI models
- **Concurrent Users**: 10+ (depending on hardware)
- **Accuracy**: Based on peer-reviewed medical literature

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Medical Disclaimer

KOYL AI provides AI-generated dietary recommendations for informational purposes only. These suggestions should not replace professional medical advice, diagnosis, or treatment. Always consult with a qualified healthcare provider before making significant dietary changes.

## 🆘 Support

For issues and questions:
1. Check the [troubleshooting guide](#troubleshooting)
2. Review [common issues](#common-issues)
3. Open an issue on GitHub

## 📈 Roadmap

- [ ] User authentication and profiles
- [ ] Recommendation history
- [ ] PDF export functionality
- [ ] Mobile app version
- [ ] Integration with fitness trackers
- [ ] Meal planning features
- [ ] Nutritionist consultation booking
