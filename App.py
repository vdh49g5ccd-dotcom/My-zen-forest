import streamlit as st
import google.generativeai as genai
import json, os, plotly.graph_objects as go

# --- הגדרות בסיסיות ---
API_KEY = "" # נשאר ריק, המפתח ב-Secrets

def setup_ai():
    api_key = st.secrets.get("API_KEY")
    if not api_key: return None
    try:
        genai.configure(api_key=api_key)
        instruction = "אתה מדריך רך ומזמין לאיש נדל''ן בירושלים. ענה בקצרה וברוגע."
        return genai.GenerativeModel("gemini-1.5-flash", system_instruction=instruction)
    except: return None

# --- ניהול נתונים ---
DATA_FILE = 'forest_data.json'
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f: return json.load(f)
        except: pass
    return {"categories": ["💎 לידים", "🏠 בלעדיות", "📖 תורה", "💰 שוק ההון"], 'history': []}

def save_data(d):
    with open(DATA_FILE, 'w', encoding='utf-8') as f: json.dump(d, f, indent=4, ensure_ascii=False)

data = load_data()

# --- תצוגת נרות (Plotly) ---
st.title("🌿 יער הנדל''ן הקסום")

fig = go.Figure()
for cat in data['categories']:
    count = len([h for h in data['history'] if h['cat'] == cat])
    fig.add_trace(go.Bar(x=[cat], y=[max(count, 0.2)], name=cat))

fig.update_layout(height=200, margin=dict(t=5, b=5, l=5, r=5), showlegend=False)
st.plotly_chart(fig, use_container_width=True)

# --- הוספת משימה וקטגוריה ---
col1, col2 = st.columns(2)
with col1:
    with st.expander("🌱 משימה חדשה"):
        c = st.selectbox("תחום", data['categories'])
        t = st.text_input("מה לעשות?")
        if st.button("שתול"):
            data['history'].append({"task": t, "cat": c})
            save_data(data)
            st.rerun()
with col2:
    with st.expander("✨ קטגוריה חדשה"):
        n = st.text_input("שם הקטגוריה")
        if st.button("הוסף"):
            data['categories'].append(n)
            save_data(data)
            st.rerun()

# --- צ'אט עם המדריך ---
prompt = st.chat_input("דבר עם המדריך...")
if prompt:
    st.chat_message("user").write(prompt)
    model = setup_ai()
    if model:
        try:
            res = model.generate_content(prompt)
            st.chat_message("assistant").write(res.text)
        except: st.error("המדריך נח... בדוק API Key.")
