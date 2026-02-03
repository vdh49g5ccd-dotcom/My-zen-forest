import streamlit as st
import google.generativeai as genai
import json, os, plotly.graph_objects as go

# הדבק כאן את המפתח הארוך שלך בתוך המרכאות
API_KEY = "AIzaSyALaJM3c1Sjt8l-eWJlVM3horh4X-wkEPY"

def setup_ai():
    try:
        genai.configure(api_key=API_KEY)
        instruction = "אתה מדריך רך ומזמין לאיש נדל''ן בירושלים. ענה בקצרה וברוגע."
        return genai.GenerativeModel("gemini-1.5-flash", system_instruction=instruction)
    except: return None

# שאר הקוד נשאר אותו דבר... (אני מקצר כאן כדי שתראה את השורה החשובה)
st.title("🌿 יער הנדל''ן")
if prompt := st.chat_input("דבר איתי..."):
    model = setup_ai()
    if model:
        res = model.generate_content(prompt)
        st.write(res.text)
