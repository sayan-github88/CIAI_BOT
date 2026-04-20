import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os



load_dotenv("API.env")

# Works locally (API.env) AND on Streamlit Cloud (secrets)
try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
except:
    groq_api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=groq_api_key)

SYSTEM_PROMPT = """
You are PharmaDesk, an AI assistant built for a Customerinsights.AI.
You are knowledgeable, professional, and concise.

You help employees across these 6 domains:

1. HR — Leave policies, onboarding, compliance, payroll FAQs
2. Marketing — Campaign ideas, brand messaging, pharma content
3. Commercial Analytics — Market sizing, KPIs, competitor benchmarking
4. Delivery — Project tracking, milestones, risk flags
5. Recruiting — Job descriptions, interview questions, candidate evaluation
6. Learning & Development — Training plans, quizzes, pharma knowledge

Always:
- Identify which domain the question belongs to and mention it
- Give practical, pharma-consulting relevant answers
- Keep responses clear and structured
- If unsure, ask a clarifying question

You are a helpful internal colleague, not a generic chatbot.
"""

st.set_page_config(page_title="PharmaDesk", page_icon="💊", layout="centered")
st.title("💊 PharmaDesk")
st.caption("Your AI colleague for HR · Marketing · Analytics · Delivery · Recruiting · L&D")

domain = st.selectbox("Select your domain (optional — helps the bot focus):",
    ["Auto-detect", "HR", "Marketing", "Commercial Analytics", "Delivery", "Recruiting", "Learning & Development"])

if "messages" in st.session_state and st.button("🗑 Clear Chat"):
    st.session_state.messages = []

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask anything — HR, Marketing, Analytics, Delivery, Recruiting or L&D..."):
    
    domain_hint = f"\n\nNote: The user has selected the domain: {domain}." if domain != "Auto-detect" else ""
    full_system = SYSTEM_PROMPT + domain_hint

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": full_system}] + st.session_state.messages,
                max_tokens=1024,
                temperature=0.7
            )
            reply = response.choices[0].message.content
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})