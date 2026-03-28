# 🥗 NutriMind – AI-Powered Smart Health Diet Assistant
An intelligent diet planning application that generates personalized meal plans using AI.

## 🔗 Live Demo
👉 https://nutrimind-ai-powered-smart-health-diet.onrender.com

## 📌 Problem Statement
Many people struggle to create personalized diet plans based on their health goals, lifestyle, and preferences.
Manual planning is time-consuming and often inaccurate.

## 💡 Solution
NutriMind uses AI to generate customized diet plans based on user input like age, weight, goals, and preferences.

## ✨ Features
- 🔐 User Authentication (Login/Signup)
- 🤖 AI-generated diet plans using Gemini API
- 📊 Personalized recommendations
- 🗄️ Data storage using MongoDB
- 🎯 Goal-based meal planning (weight loss, gain, etc.)
- 📱 Responsive UI with Streamlit

## 🛠️ Tech Stack
Frontend: Streamlit  
Backend: FastAPI  
Database: MongoDB  
AI: Google Gemini API  
Authentication: JWT + Bcrypt  
Deployment: Render

## 🧠 How It Works
1. User signs up or logs in
2. Enters personal details (age, weight, goal)
3. Backend sends data to Gemini AI
4. AI generates a diet plan
5. Plan is stored in MongoDB and displayed on UI

## 📂 Project Structure
backend/
 ├── app.py
 ├── requirements.txt

frontend/
 ├── diet_app.py

.env
README.md

## ⚙️ Installation
### Clone the repository
git clone https://github.com/your-username/nutrimind.git
### Backend Setup
cd backend
pip install -r requirements.txt
uvicorn app:app --reload
### Frontend Setup
cd frontend
streamlit run diet_app.py

## 🔑 Environment Variables
Create a `.env` file and add:
GEMINI_API_KEY=your_api_key
MONGO_URI=your_mongodb_url
SECRET_KEY=your_secret_key

## 📈 Future Improvements
- Add calorie tracking dashboard
- Mobile app version
- Integration with fitness devices

## 🤝 Contributing
Feel free to fork and contribute to this project.

## 🙌 Acknowledgements
Special thanks to Omkar Sir  for guidance and inspiration.