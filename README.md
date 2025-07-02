# koly-health-diet-partner

# 🚀 KOYL AI – Comprehensive Nutrition Intelligence System

![Overview](https://github.com/Rajatkapoor01/koly-health-diet-partner-/blob/main/Overview01.png)

> **KOYL AI** is an AI-powered healthcare project designed to provide **personalized dietary recommendations** based on user symptoms and food allergies. It bridges the gap between clinical research and daily nutrition using advanced NLP models and a user-friendly interface.

---

## 🧠 What is KOYL AI?

KOYL AI is a **comprehensive, AI-driven dietary recommendation system** that combines **medical-grade data**, **semantic AI models**, and **real-time personalization** to deliver intelligent nutrition advice. It ensures safety, accuracy, and simplicity for users from all backgrounds.


## 🔗 LinkedIn Showcase Post

📢 I shared KOYL AI on LinkedIn with a short demo and detailed explanation.  
Check out the post and support the project here:

🔗 [View LinkedIn Post](https://www.linkedin.com/posts/rajat-kapoor-732042289_techbitsolution-ai-nutritiontech-activity-7346088626650234880-KwzJ?utm_source=share&utm_medium=member_desktop&rcm=ACoAAEXzZZYBc42b4Y4-PLTTOsb3mW-3GVYGrxI) 

> 💬 Feel free to drop your thoughts, feedback, or suggestions in the comments!

> 📹 Click the image above to watch the short demo video.


---

## 🎯 Key Features

### ✅ Medical-Grade Intelligence
- Integrated with **PubMed, USDA, EatRight.org**, and **Harvard Nutrition**
- Over **1000+ research papers** indexed for evidence-based suggestions

### ✅ Personalized Dietary Plans
- Custom recommendations based on **user symptoms and allergies**
- Covers **medical conditions** like diabetes, inflammation, cardiovascular, and digestive issues

### ✅ Allergy Filtering
- Robust **smart filter system** to remove risky foods and suggest safe alternatives

### ✅ AI-Powered Backend
- Uses **Sentence-BERT** for semantic understanding
- **T5 Transformer** for natural language generation
- **FAISS** vector search for lightning-fast retrieval

### ✅ Professional UI (Frontend)
- Built with **Next.js 14**, **TypeScript**, and **Tailwind CSS**
- Uses **shadcn/ui** for modern UI components
- Responsive across devices (desktop & mobile)

---

## 🖥️ Screenshots

### 🔍 System Overview

![Overview 2](https://github.com/Rajatkapoor01/koly-health-diet-partner-/blob/main/Overview02.png)

### 🗂️ Task Files & Structure

![Task Files](https://github.com/Rajatkapoor01/koly-health-diet-partner-/blob/main/task%20fileOverview.png)

---
### 📽️ **File Overview Demo**

[![Watch Video Demo](https://github.com/Rajatkapoor01/koly-health-diet-partner-/blob/main/Overview01.png)](https://github.com/Rajatkapoor01/koly-health-diet-partner-/blob/main/Short%20For%20Work.mp4)

---
🧰 Tech Stack Used
🚀 Frontend
Next.js 14 – Framework for React with App Router and server-side rendering

React.js – Library for building user interfaces

TypeScript – Strongly typed language for better developer experience

Tailwind CSS – Utility-first CSS framework for responsive styling

shadcn/ui – Modern, accessible UI components for Next.js

🧠 Backend
Python Flask – Lightweight web framework for RESTful APIs

Sentence-BERT (sBERT) – Transformer model for semantic similarity and search

T5 Transformer – For text generation and summarization

FAISS – Facebook AI similarity search for fast vector indexing

NumPy & PyTorch – For computation and deep learning pipeline support

🔗 API & Middleware
REST API – JSON-based communication between frontend and backend

Next.js API Routes – Middleware for request validation, error handling, and fallback logic

CORS – Cross-origin resource sharing configuration for secure communication

🧪 Testing & Validation
Mock Responses – Offline fallback with mock data when backend is unavailable

Error Handling – Custom error messages and fallback states for stability

Input Validation – On both frontend and backend to sanitize and validate user data

⚙️ DevOps & Configuration
Environment Variables – .env configuration for production and development

Health Check Endpoints – For backend service monitoring and failover

Responsive Design – Mobile-first approach for cross-device compatibility


## 🏗️ Project Architecture

```text
User Input
   ↓
Next.js Frontend (React + TS)
   ↓
API Route Layer (Validation + Fallback)
   ↓
Flask Backend (AI Processing)
   ↓
RAG Pipeline (Semantic Search + Generation)
   ↓
Response (Recommendations + Sources)
   ↓
Frontend Display
🔧 Tech Stack

Offline fallback mode

Health check endpoints

Config via .env for dev & prod

📌 Highlights
🔬 Evidence-Based AI: Every recommendation is linked to real medical literature

🛡️ User Safety First: Allergy detection and medical disclaimer system in place

💡 Offline Support: Works even when backend is down (mock responses)

📚 Source Attribution: Clearly shows where each recommendation comes from

🧪 Tested & Reliable: Includes error handling, testing suite, and full documentation

📁 Repository Structure
text
Copy
Edit
├── app/ (Frontend - Next.js)
│   ├── api/recommend/route.ts
│   ├── components/
│   └── pages/
├── scripts/backend/ (Flask Backend)
│   ├── app.py
│   ├── rag_pipeline.py
│   └── utils/
├── public/
├── README.md
└── .env.example
📝 Future Enhancements
🧑‍⚕️ Integration with wearable health data (Fitbit, Apple Health)

📆 Weekly meal scheduling

📊 Nutrition progress analytics

🌎 Multi-language support

📱 Mobile app version

🧑‍💻 Developed By
Rajat Kapoor
🔗 GitHub Profile
📧 rajatkapoor.dev@gmail.com

📌 This project is for educational.
