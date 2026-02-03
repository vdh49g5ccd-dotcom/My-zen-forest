import streamlit as st
import google.generativeai as genai
import json, os, plotly.graph_objects as go

# הדבק כאן את המפתח הארוך שלך בתוך המרכאות
API_KEY = ""
def setup_ai():
    # שורה קריטית: מחפשת את המפתח ב"כספת" (Secrets)
    api_key = API_KEY if API_KEY else st.secrets.get("API_KEY")
    if not api_key:
        return None
    try:
        genai.configure(api_key=api_key)
        instruction = """
        אתה המדריך של 'יער המשימות הקסום', מלווה רוחני ועסקי לאיש נדל"ן בירושלים.
        הגישה שלך רכה ומזמינה מאוד. אתה שואל שאלות מעוררות מחשבה במקום לתת פקודות.
        עזור למשתמש למצוא איזון בין עולם הנדל"ן לעולם הרוח והנפש.
        """
        return genai.GenerativeModel("gemini-1.5-flash", system_instruction=instruction)
    except:
        return None

# שאר הקוד נשאר אותו דבר... (אני מקצר כאן כדי שתראה את השורה החשובה)
st.title("🌿 יער הנדל''ן")
if prompt := st.chat_input("דבר איתי..."):
    model = setup_ai()
    if model:
        res = model.generate_content(prompt)
        st.write(res.text)
