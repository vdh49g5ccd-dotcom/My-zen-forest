import streamlit as st
import google.generativeai as genai
import json, os, plotly.graph_objects as go

# --- 1. הגדרות בסיסיות ---
# השאר את זה ריק, המפתח נמשך מה-Secrets
API_KEY = ""

def setup_ai():
    # משיכת המפתח מהכספת של Streamlit
    api_key = st.secrets.get("API_KEY")
    if not api_key:
        return None
    try:
        genai.configure(api_key=api_key)
        # הנחיות למדריך: רך, מזמין ושואל שאלות
        instruction = "אתה מדריך רך ומזמין לאיש נדל''ן בירושלים. ענה בקצרה וברוגע ושאל שאלות."
        # שימוש במודל gemini-1.5-flash פותר את שגיאת ה-NotFound
        return genai.GenerativeModel("gemini-1.5-flash", system_instruction=instruction)
    except:
        return None

# --- 2. ניהול נתונים ---
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

# --- 3. תצוגת נרות (הגרף שרצית) ---
st.title("🌿 יער הנדל''ן הקסום")

# יצירת גרף הנרות
fig = go.Figure()
colors = ['#81c784', '#ffb74d', '#4fc3f7', '#ba68c8']

for i, cat in enumerate(data['categories']):
    # ספירת משימות שבוצעו בכל קטגוריה
    done_count = len([h for h in data['history'] if h['cat'] == cat])
    fig.add_trace(go.Bar(
        x=[cat], 
        y=[max(done_count, 0.5)], # גובה מינימלי כדי שהנר ייראה
        marker=dict(color=colors[i % len(colors)]),
        name=cat
    ))

fig.update_layout(
    height=250, 
    margin=dict(t=10, b=10, l=10, r=10), 
    paper_bgcolor='rgba(0,0,0,0)', 
    plot_bgcolor='rgba(0,0,0,0)',
    showlegend=False
)
st.plotly_chart(fig, use_container_width=True)

# --- 4. הוספת משימה וקטגוריה ---
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    with st.expander("🌱 משימה חדשה"):
        c = st.selectbox("בחר תחום", data['categories'])
        t = st.text_input("מה המשימה?")
        if st.button("שתול משימה"):
            if t:
                data['history'].append({"task": t, "cat": c})
                save_data(data)
                st.success("נשתל!")
                st.rerun()

with col2:
    with st.expander("✨ קטגוריה חדשה"):
        n = st.text_input("שם הקטגוריה")
        if st.button("הוסף נר"):
            if n and n not in data['categories']:
                data['categories'].append(n)
                save_data(data)
                st.rerun()

# --- 5. צ'אט עם המדריך ---
st.markdown("---")
prompt = st.chat_input("דבר עם המדריך...")
if prompt:
    st.chat_message("user").write(prompt)
    model = setup_ai()
    if model:
        try:
            res = model.generate_content(prompt)
            st.chat_message("assistant").write(res.text)
        except Exception as e:
            st.error(f"המדריך נח... (שגיאה: {str(e)})")
    else:
        st.info("אנא וודא שהמפתח (API_KEY) נמצא ב-Secrets.")
