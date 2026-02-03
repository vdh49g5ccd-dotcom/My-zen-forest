import streamlit as st
import google.generativeai as genai
import json, os, plotly.graph_objects as go

# --- 1. הגדרות API (מושך מה-Secrets) ---
API_KEY = "" # השאר ריק, המערכת תמשוך מהכספת

def setup_ai():
    # חיבור לכספת ה-Secrets של Streamlit
    api_key = API_KEY if API_KEY else st.secrets.get("API_KEY")
    if not api_key:
        return None
    try:
        genai.configure(api_key=api_key)
        # הנחיות למדריך: רך, מזמין, שואל שאלות ומאזן בין נדל"ן לרוח
        instruction = """
        אתה המדריך של 'יער המשימות הקסום', מלווה רוחני ועסקי לאיש נדל"ן בירושלים.
        הגישה שלך רכה ומזמינה מאוד. אתה שואל שאלות מעוררות מחשבה במקום לתת פקודות.
        עזור למשתמש למצוא איזון בין עולם הנדל"ן (לידים, סגירות) לעולם הרוח והנפש.
        """
        # שימוש במודל gemini-1.5-flash פותר את שגיאת ה-NotFound
        return genai.GenerativeModel("gemini-1.5-flash", system_instruction=instruction)
    except:
        return None

# --- 2. ניהול נתונים (שמירה בתוך הקובץ) ---
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
if 'data' not in st.session_state:
    st.session_state.data = load_data()
data = st.session_state.data

# --- 3. עיצוב ותצוגת נרות (Plotly) ---
st.markdown('<style>.stApp { background-color: #0e1117; color: white; }</style>', unsafe_allow_html=True)
st.title("🌿 יער המשימות הקסום")

# יצירת גרף הנרות הצבעוני
fig = go.Figure()
colors = ['#81c784', '#ffb74d', '#4fc3f7', '#ba68c8', '#fff176']

for i, cat in enumerate(data['categories']):
    tasks = data['tasks_dict'].get(cat, [])
    # גובה הנר נקבע לפי מספר המשימות (מינימום 0.3 כדי שיראו אותו)
    height = len(tasks) if tasks else 0.3
    fig.add_trace(go.Bar(
        x=[cat], y=[height], 
        marker_color=colors[i % len(colors)],
        text="💎" if len(tasks) > 0 else "🌱",
        textposition='inside',
        name=cat
    ))

fig.update_layout(
    height=220, margin=dict(t=10, b=10, l=10, r=10),
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    showlegend=False, dragmode=False
)
fig.update_xaxes(tickfont=dict(color='white', size=12), fixedrange=True)
fig.update_yaxes(showticklabels=False, showgrid=False, fixedrange=True)
st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# --- 4. מערכת שתילת משימות ---
st.markdown("### 🌱 שתול משימה חדשה")
col1, col2 = st.columns([2, 1])
with col2:
    cat_choice = st.selectbox("בחר תחום:", data['categories'])
with col1:
    task_text = st.text_input("מה המשימה שלך?")

if st.button("שתול ביער 🚀"):
    if task_text:
        if cat_choice not in data['tasks_dict']:
            data['tasks_dict'][cat_choice] = []
        data['tasks_dict'][cat_choice].append(task_text)
        save_data(data)
        st.success(f"המשימה נשתלה ב-{cat_choice}!")
        st.rerun()

# --- 5. שיחה עם המדריך ---
st.markdown("---")
st.subheader("💬 המדריך של היער")
if prompt := st.chat_input("דבר איתי על הנדל''ן, התורה או היום שלך..."):
    with st.chat_message("user"):
        st.write(prompt)
    
    model = setup_ai()
    if model:
        try:
            # יצירת תשובה מה-AI
            res = model.generate_content(prompt)
            with st.chat_message("assistant"):
                st.write(res.text)
        except Exception as e:
            st.error("המדריך נח כרגע... וודא שהמפתח ב-Secrets תקין.")
    else
