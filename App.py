import streamlit as st
import google.generativeai as genai
import json, os, plotly.graph_objects as go

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
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f: return json.load(f)
        except: pass
    return {"categories": ["💎 לידים", "🏠 בלעדיות", "📢 שיווק", "📖 תורה", "💪 אנרגיה"], 'history': []}

def save_data(d):
    with open(DATA_FILE, 'w', encoding='utf-8') as f: json.dump(d, f, indent=4, ensure_ascii=False)

st.set_page_config(page_title="Zen Forest", layout="centered")
data = load_data()

# --- עיצוב משחקי משופר ---
st.markdown('''
<style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), 
                    url("https://images.unsplash.com/photo-1518137319011-8c88a1793ba9?q=80&w=2070");
        background-size: cover;
        background-attachment: fixed;
    }
    .main-box {
        background-color: rgba(255, 255, 255, 0.95);
        padding: 20px;
        border-radius: 20px;
        border: 2px solid #4caf50;
        color: #1b5e20;
    }
    h1 { color: #ffffff !important; text-shadow: 2px 2px 4px #000; text-align: center; font-size: 2.5rem; }
    .stButton>button {
        background-color: #2e7d32 !important;
        color: white !important;
        border-radius: 50px;
        height: 3.5em;
        font-weight: bold;
        width: 100%;
    }
</style>
''', unsafe_allow_html=True)

st.title("🌿 יער הנדל''ן הקסום")

# --- גרף קריסטלים (תיקון ה-Layout) ---
fig = go.Figure()
colors = ['#81c784', '#ffb74d', '#4fc3f7', '#ba68c8', '#fff176']

for i, cat in enumerate(data['categories']):
    done_count = len([h for h in data['history'] if h['cat'] == cat])
    fig.add_trace(go.Bar(
        x=[cat], y=[max(done_count, 0.5)],
        marker=dict(color=colors[i % len(colors)], line=dict(color='white', width=2)),
        text="💎" if done_count > 0 else "🌱",
        textposition='inside',
        showlegend=False
    ))

# תיקון השגיאה: הגדרת הנעילה בצורה מפורשת ופשוטה יותר
fig.update_xaxes(fixedrange=True, tickfont=dict(color='white', size=14, bold=True))
fig.update_yaxes(fixedrange=True, showticklabels=False, showgrid=False)
fig.update_layout(
    height=350,
    margin=dict(t=10, b=10, l=10, r=10),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(255,255,255,0.1)',
    dragmode=False # מבטל אפשרות גרירה וזום
)

st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# --- ממשק פעולה ---
st.markdown('<div class="main-box">', unsafe_allow_html=True)
active_cats = [c for c in data['categories'] if data.get(c, {}).get('tasks')]

if active_cats:
    target = st.selectbox("מה כבשת עכשיו?", active_cats)
    if st.button("סיימתי! 🚀"):
        task = data[target]['tasks'].pop(0)
        data['history'].append({"task": task['title'], "cat": target})
        save_data(data)
        st.balloons()
        st.rerun()
else:
    st.write("היער מחכה למשימות חדשות... 🌱")

with st.expander("➕ שתילת משימה חדשה"):
    c_new = st.selectbox("תחום", data['categories'])
    t_new = st.text_input("מה המשימה?")
    if st.button("שתול 🌱"):
        if t_new:
            if c_new not in data: data[c_new] = {"tasks": []}
            data[c_new]['tasks'].append({"title": t_new})
            save_data(data)
            st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# צ'אט
if prompt := st.chat_input("דבר עם מדריך היער..."):
    with st.chat_message("user"): st.write(prompt)
    model = setup_ai()
    if model:
        try:
            res = model.generate_content(f"מצב יער: {data}. משתמש: {prompt}")
            with st.chat_message("assistant"): st.write(res.text)
        except: st.error("המדריך נח...")
