import streamlit as st
import google.generativeai as genai
import json, os, plotly.graph_objects as go

# --- 1. המוח של ה-AI (הנחיות המדריך הרך) ---
# כאן תדביק את המפתח שתייצר ב-Google AI Studio
API_KEY == "AIzaSyALaJM3c1Sjt8l-eWJlVM3horh4X-wkEPY"

def setup_ai():
    if API_KEY == "הדבק_כאן_את_המפתח_שלך":
        return None
    try:
        genai.configure(api_key=API_KEY)
        # כאן הכנסתי את הזהות שביקשת - רכה, שואלת ומאזנת
        instruction = """
        אתה המדריך של 'יער המשימות הקסום', מלווה רוחני ועסקי לאיש נדל"ן.
        הגישה שלך רכה ומזמינה, אתה שואל שאלות מעוררות מחשבה במקום לתת פקודות.
        אתה עוזר למצוא איזון בין נדל"ן, לימוד תורה והתפתחות אישית.
        התמקד בצעד הבא הקטן של 5 דקות.
        """
        return genai.GenerativeModel("gemini-1.5-flash", system_instruction=instruction)
    except: return None

# --- 2. ניהול נתונים ---
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

# --- 3. עיצוב הממשק ---
st.markdown('''
<style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                    url("https://images.unsplash.com/photo-1518137319011-8c88a1793ba9?q=80&w=2070");
        background-size: cover; background-attachment: fixed;
    }
    .main-box { background-color: rgba(255, 255, 255, 0.95); padding: 15px; border-radius: 15px; color: #1b5e20; }
    .stButton>button { background-color: #2e7d32 !important; color: white !important; border-radius: 50px; }
</style>
''', unsafe_allow_html=True)

st.title("🌿 יער הנדל''ן הקסום")

# --- 4. גרף נרות קטנים (צומצם ל-200 פיקסלים) ---
fig = go.Figure()
colors = ['#81c784', '#ffb74d', '#4fc3f7', '#ba68c8', '#fff176', '#f06292', '#4db6ac']

for i, cat in enumerate(data['categories']):
    done_count = len([h for h in data['history'] if h['cat'] == cat])
    fig.add_trace(go.Bar(
        x=[cat], y=[max(done_count, 0.3)],
        marker=dict(color=colors[i % len(colors)]),
        text="💎" if done_count > 0 else "🌱",
        textposition='inside', showlegend=False
    ))

fig.update_xaxes(fixedrange=True, tickfont=dict(color='white', size=12))
fig.update_yaxes(fixedrange=True, showticklabels=False, showgrid=False)
fig.update_layout(height=200, margin=dict(t=5, b=5, l=5, r=5), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', dragmode=False)
st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# --- 5. ממשק פעולה ושתילה ---
st.markdown('<div class="main-box">', unsafe_allow_html=True)

# ביצוע משימה
active_cats = [c for c in data['categories'] if data.get(c, {}).get('tasks')]
if active_cats:
    target = st.selectbox("מה כבשת עכשיו?", active_cats)
    if st.button("סיימתי! 🚀"):
        task = data[target]['tasks'].pop(0)
        data['history'].append({"task": task['title'], "cat": target})
        save_data(data)
        st.balloons()
        st.rerun()

# הוספת משימה או קטגוריה חדשה
col1, col2 = st.columns(2)
with col1:
    with st.expander("🌱 משימה חדשה"):
        c_task = st.selectbox("באיזה תחום?", data['categories'])
        t_task = st.text_input("מה המשימה?")
        if st.button("שתול משימה"):
            if t_task:
                if c_task not in data: data[c_task] = {"tasks": []}
                data[c_task]['tasks'].append({"title": t_task})
                save_data(data)
                st.rerun()

with col2:
    with st.expander("✨ קטגוריה חדשה"):
        new_cat = st.text_input("שם הקטגוריה (למשל: שוק ההון)")
        if st.button("צור נר חדש"):
            if new_cat and new_cat not in data['categories']:
                data['categories'].append(new_cat)
                save_data(data)
                st.success(f"הנר {new_cat} נוסף ליער!")
                st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# --- 6. הצ'אט עם המדריך ---
if prompt := st.chat_input("דבר עם המדריך..."):
    with st.chat_message("user"): st.write(prompt)
    model = setup_ai()
    if model:
        try:
            res = model.generate_content(f"מצב יער: {data}. משתמש: {prompt}")
            with st.chat_message("assistant"): st.write(res.text)
        except Exception as e:
            st.error("המדריך נח כרגע (בדוק API Key או מכסה).")
    else:
        st.info("כדי שהמדריך יענה, עליך להדביק את ה-API Key בקוד ב-GitHub.")
