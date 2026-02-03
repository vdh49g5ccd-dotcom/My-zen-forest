import streamlit as st
import google.generativeai as genai
import json, os, plotly.graph_objects as go

# --- 1. הגדרות בסיס ---
API_KEY = "" # נשאר ריק כי המפתח ב-Secrets

def setup_ai():
    api_key = API_KEY if API_KEY else st.secrets.get("API_KEY")
    if not api_key: return None
    try:
        genai.configure(api_key=api_key)
        instruction = "אתה מדריך רך ומזמין לאיש נדל''ן בירושלים. עזור לו לאזן בין עבודה לרוח."
        return genai.GenerativeModel("gemini-1.5-flash", system_instruction=instruction)
    except: return None

# --- 2. ניהול נתונים ---
DATA_FILE = 'forest_data.json'
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f: return json.load(f)
        except: pass
    return {"categories": ["💎 לידים", "🏠 בלעדיות", "📢 שיווק", "📖 תורה", "💰 שוק ההון"], 'history': [], 'tasks_dict': {}}

def save_data(d):
    with open(DATA_FILE, 'w', encoding='utf-8') as f: json.dump(d, f, indent=4, ensure_ascii=False)

st.set_page_config(page_title="Zen Forest", layout="centered")
if 'data' not in st.session_state: st.session_state.data = load_data()
data = st.session_state.data

# --- 3. גרף הנרות (התצוגה שחיפשת) ---
st.title("🌿 יער המשימות הקסום")
fig = go.Figure()
colors = ['#81c784', '#ffb74d', '#4fc3f7', '#ba68c8', '#fff176']

for i, cat in enumerate(data['categories']):
    tasks = data['tasks_dict'].get(cat, [])
    height = len(tasks) if tasks else 0.3
    fig.add_trace(go.Bar(x=[cat], y=[height], marker_color=colors[i % len(colors)], name=cat))

fig.update_layout(height=200, margin=dict(t=0, b=0, l=0, r=0), showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
fig.update_xaxes(tickfont=dict(color='white'))
st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# --- 4. הטמעת משימות חדשות ---
with st.expander("🌱 שתילת משימה חדשה"):
    col1, col2 = st.columns([2, 1])
    with col2: cat_choice = st.selectbox("תחום", data['categories'])
    with col1: task_text = st.text_input("מה המשימה?")
    if st.button("שתול ביער"):
        if task_text:
            if cat_choice not in data['tasks_dict']: data['tasks_dict'][cat_choice] = []
            data['tasks_dict'][cat_choice].append(task_text)
            save_data(data)
            st.rerun()

# --- 5. הצ'אט עם המדריך ---
st.subheader("💬 שיחה עם המדריך")
if prompt := st.chat_input("דבר איתי..."):
    with st.chat_message("user"): st.write(prompt)
    model = setup_ai()
    if model:
        try:
            res = model.generate_content(prompt)
            with st.chat_message("assistant"): st.write(res.text)
        except: st.error("המדריך נח... בדוק את המפתח ב-Secrets")
    else: st.warning("המפתח לא הוגדר ב-Secrets")
