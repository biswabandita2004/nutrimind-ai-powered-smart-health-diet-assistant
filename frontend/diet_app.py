import streamlit as st
import requests
import re
import plotly.express as px
import pyttsx3
from fpdf import FPDF

API_URL = "https://nutrimind-ai-powered-smart-health-diet.onrender.com"

st.set_page_config(page_title="AI Diet Planner", page_icon="🥗", layout="wide")

def safe_json(res):
    try:
        return res.json()
    except:
        st.error("❌ Backend error")
        st.write(res.text)
        return None

def clean_text(text):
    text = re.sub(r'[#*`_>-]', '', text)
    text = re.sub(r'\n+', ' ', text)
    return text.strip()

if "engine" not in st.session_state:
    engine = pyttsx3.init()
    engine.setProperty('rate', 180)
    st.session_state.engine = engine

st.sidebar.title("🔐 Authentication")
menu = st.sidebar.selectbox("Select", ["Login", "Signup"])

if menu == "Signup":
    name = st.sidebar.text_input("Name")
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Signup"):
        res = requests.post(f"{API_URL}/signup", json={
            "name": name,
            "email": email,
            "password": password
        })

        data = safe_json(res)
        if data:
            st.sidebar.success(data)

elif menu == "Login":
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        res = requests.post(f"{API_URL}/login", json={
            "email": email,
            "password": password
        })

        data = safe_json(res)

        if data and "access_token" in data:
            st.session_state["token"] = data["access_token"]
            st.sidebar.success("Login successful ✅")
        else:
            st.sidebar.error("Login failed ❌")

if "token" not in st.session_state:
    st.warning("⚠️ Please login first")
    st.stop()

st.title("🥗 AI Personal Diet Planner")
st.success("🚀 Powered by FastAPI + MongoDB + AI")

col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age", 10, 100, 25)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    height = st.number_input("Height (cm)", 100, 250, 170)
    weight = st.number_input("Weight (kg)", 30, 200, 65)

with col2:
    goal = st.selectbox("Goal", ["Weight Loss", "Weight Gain", "Muscle Gain", "Maintain"])
    food_type = st.selectbox("Food Type", ["Vegetarian", "Non-Vegetarian", "Vegan"])
    activity = st.selectbox("Activity", ["Sedentary", "Light", "Moderate", "Active"])

bmi = round(weight / ((height / 100) ** 2), 2)
st.subheader(f"📉 BMI: {bmi}")

if st.button("🚀 Generate Diet Plan"):
    res = requests.post(
        f"{API_URL}/generate-diet",
        json={
            "age": age,
            "gender": gender,
            "height": height,
            "weight": weight,
            "goal": goal,
            "food_type": food_type,
            "activity": activity
        },
        headers={"Authorization": f"Bearer {st.session_state['token']}"}
    )

    data = safe_json(res)

    if data and "diet_plan" in data:
        st.session_state["output"] = data["diet_plan"]

output = st.session_state.get("output")

if output:
    st.markdown("## 🥗 Your Diet Plan")
    st.write(output)

if st.button("🔊 Speak Diet Plan"):
    if output:
        engine = st.session_state.engine
        engine.say(output)
        engine.runAndWait()
    else:
        st.warning("No diet plan available to speak.")

st.subheader("💬 Ask Nutrition Bot")

if "chat_reply" not in st.session_state:
    st.session_state.chat_reply = ""

question = st.text_input("Ask something")

if st.button("Ask"):
    if question.strip() == "":
        st.warning("Please enter a question")
    else:
        res = requests.post(
            f"{API_URL}/chat",
            json={"question": question},
            headers={"Authorization": f"Bearer {st.session_state['token']}"}
        )

        data = safe_json(res)

        if data and "reply" in data:
            st.session_state.chat_reply = data["reply"]
        else:
            st.session_state.chat_reply = "❌ No response from backend"

if st.session_state.chat_reply:
    st.markdown("### 🤖 Answer:")
    st.write(st.session_state.chat_reply)

def extract_macros(text):
    p = c = f = 0

    match = re.search(r'protein:\s*(\d+)', text)
    if match: p = int(match.group(1))

    match = re.search(r'carbs:\s*(\d+)', text)
    if match: c = int(match.group(1))

    match = re.search(r'fats:\s*(\d+)', text)
    if match: f = int(match.group(1))

    return p, c, f

if output:
    p, c, f = extract_macros(output)

    if p or c or f:
        df = {
            "Macro": ["Protein", "Carbs", "Fats"],
            "Value": [p, c, f]
        }

        fig = px.pie(df, names="Macro", values="Value")
        st.plotly_chart(fig)

if st.button("📄 Download PDF"):
    if output:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=10)

        for line in output.split("\n"):
            pdf.multi_cell(0, 5, line)

        pdf.output("report.pdf")

        with open("report.pdf", "rb") as f:
            st.download_button("Download PDF", f, "diet.pdf")

if st.sidebar.button("Logout"):
    st.session_state.clear()
    st.sidebar.success("Logged out")