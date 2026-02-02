import streamlit as st
import google.generativeai as genai
import json, os, plotly.graph_objects as go
from datetime import datetime

# --- הגדרת המוח ---
API_KEY = "הדבק_כאן_את_המפתח_שלך"

def setup_ai():
    try:
        genai.configure(api_key=API_KEY)
        return genai.GenerativeModel("gemini-1.5-flash")
    except: return None

DATA_FILE = 'forest_data.json'
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f: return json.load(f)
    return {"categories": ["💎 לידים", "🏠 בלעדיות", "📢 שיווק", "📖 תורה", "💪 אנרגיה"], 'history': []}

def save_data(d):
    with open(DATA_FILE, 'w', encoding='utf-8') as f: json.dump(d, f, indent=4, ensure_ascii=False)

# התאמה למובייל - מסך מלא ונעים
st.set_page_config(page_title="Zen Forest", layout="centered")
data = load_data()

# עיצוב מותאם לאייפון - כפתורים גדולים וצבעי יער
st.markdown('''
<style>
    .stApp {
        background: linear-gradient(to bottom, #e8f5e9, #c8e6c9);
    }
    .main-button {
        background-color: #4caf50 !important;
        color: white !important;
        height: 60px;
        font-size: 20px !important;
        border-radius: 15px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .stSelectbox label, .stTextInput label {
        color: #2e7d32 !important;
        font-weight: bold;
    }
</style>
''', unsafe_allow_html=True)

st.title("🌿 יער הנדל''ן שלי")

# גרף קריסטלים - מוקטן למסך אייפון
fig = go.Figure()
colors = ['#66bb6a', '#ffa726', '#29b6f6', '#ab47bc', '#ffee58']

for i, cat in enumerate(data['categories']):
    done_count = len([h for h in data['history'] if h['cat'] == cat])
    fig.add_trace(go.Bar(
        x=[cat], y=[done_count if done_count > 0 else 0.5],
        marker_color=colors[i % len(colors)],
        text="💎" if done_count > 0 else "🌱",
        textposition='inside',
        showlegend=False
    ))

fig.update_layout(height=300, margin=dict(t=10, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# אזור פעולה מהיר - הכי נוח לאגודל באייפון
st.write("---")
active = [c for c in data['categories'] if data.get(c, {}).get('tasks')]
if active:
    target = st.selectbox("מה סגרת?", active)
    if st.button("סיימתי! 🏆", use_container_width=True):
        task = data[target]['tasks'].pop(0)
        data['history'].append({"task": task['title'], "cat": target})
        save_data(data); st.balloons(); st.rerun()
else:
    st.info("אין משימות. הוסף אחת למטה 👇")

with st.expander("➕ הוסף משימה חדשה"):
    c_new = st.selectbox("תחום", data['categories'])
    t_new = st.text_input("מה המשימה?")
    if st.button("שתול 🌱"):
        if c_new not in data: data[c_new] = {"tasks": []}
        data[c_new]['tasks'].append({"title": t_new}); save_data(data); st.rerun()

# צ'אט המאמן
if prompt := st.chat_input("דבר איתי..."):
    with st.chat_message("user"): st.write(prompt)
    model = setup_ai()
    if model:
        res = model.generate_content(f"מצב יער: {data}. הודעה: {prompt}")
        with st.chat_message("assistant"): st.write(res.text)
