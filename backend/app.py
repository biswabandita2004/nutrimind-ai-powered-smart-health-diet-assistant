from fastapi import FastAPI, Header
import google.generativeai as genai
import os
from dotenv import load_dotenv
from pymongo import MongoClient

from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

from fastapi.middleware.cors import CORSMiddleware

# -------------------- CONFIG --------------------
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# MongoDB
client = MongoClient(os.getenv("MONGO_URI"))
db = client["diet_db"]

plans_collection = db["plans"]
users_collection = db["users"]

# Auth
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# -------------------- ROUTES --------------------

@app.get("/")
def home():
    return {"message": "Backend is running 🚀"}

# -------------------- SIGNUP --------------------
@app.post("/signup")
def signup(data: dict):
    password = data["password"][:72]  # ✅ FIX

    if users_collection.find_one({"email": data["email"]}):
        return {"error": "User already exists"}

    hashed_password = pwd_context.hash(password)

    users_collection.insert_one({
        "name": data["name"],
        "email": data["email"],
        "password": hashed_password
    })

    return {"message": "User created successfully"}

# -------------------- LOGIN --------------------
@app.post("/login")
def login(data: dict):
    password = data["password"][:72]  # ✅ FIX

    user = users_collection.find_one({"email": data["email"]})

    if not user:
        return {"error": "User not found"}

    if not pwd_context.verify(password, user["password"]):
        return {"error": "Wrong password"}

    token = jwt.encode(
        {
            "email": user["email"],
            "exp": datetime.utcnow() + timedelta(hours=1)
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {"access_token": token}

# -------------------- GENERATE DIET --------------------
@app.post("/generate-diet")
def generate_diet(data: dict):
    try:
        bmi = round(data['weight'] / ((data['height'] / 100) ** 2), 2)

        prompt = f"""
You are a professional dietician AI.

Give clean text only.

Include:
Breakfast
Lunch
Dinner
Snacks

Also include:
protein: number
carbs: number
fats: number

User Details:
Age: {data['age']}
Gender: {data['gender']}
Height: {data['height']}
Weight: {data['weight']}
BMI: {bmi}
Goal: {data['goal']}
Food Type: {data['food_type']}
Activity: {data['activity']}
"""

        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)

        diet_text = response.text

        plans_collection.insert_one({
            "age": data['age'],
            "gender": data['gender'],
            "height": data['height'],
            "weight": data['weight'],
            "bmi": bmi,
            "goal": data['goal'],
            "food_type": data['food_type'],
            "activity": data['activity'],
            "diet_plan": diet_text
        })

        return {"diet_plan": diet_text}

    except Exception as e:
        return {"error": str(e)}

# -------------------- CHAT --------------------
@app.post("/chat")
def chat(data: dict, authorization: str = Header(None)):
    try:
        question = data.get("question")

        prompt = f"""
You are a professional nutrition assistant.

User question: {question}

Answer clearly and concisely.
"""

        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)

        return {"reply": response.text}

    except Exception as e:
        return {"error": str(e)}