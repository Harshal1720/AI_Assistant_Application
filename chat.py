import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Setup Gemini
load_dotenv(override=True)
gemini_api_key = os.getenv('GOOGLE_API_KEY') # Ensure this is set in your .env
genai.configure(api_key=gemini_api_key)

# Configure the model
# Using 1.5 Flash for speed, or 'gemini-1.5-pro' for more complex reasoning
model = genai.GenerativeModel('gemini-2.5-flash')

st.set_page_config(page_title="Puneri Pattern | AI Mentor", page_icon="logo.png", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0e1117 0%, #161b22 100%); color: #ffffff; }
    section[data-testid="stSidebar"] { background-color: rgba(255, 255, 255, 0.05) !important; border-right: 1px solid rgba(255, 255, 255, 0.1); }
    [data-testid="stMetricValue"] { color: #00d4ff !important; font-weight: 700; text-shadow: 0px 0px 10px rgba(0, 212, 255, 0.3); }
    .stButton>button { width: 100%; border-radius: 12px; border: 1px solid #00d4ff; background-color: transparent; color: #00d4ff; transition: all 0.3s ease; }
    .stButton>button:hover { background-color: #00d4ff; color: #0e1117; box-shadow: 0px 0px 15px rgba(0, 212, 255, 0.5); }
    .stChatMessage { background-color: rgba(255, 255, 255, 0.03) !important; border-radius: 15px; margin-bottom: 10px; border: 1px solid rgba(255, 255, 255, 0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("logo.png", width=500)
    st.title("Puneri Pattern")
    st.markdown("---")
    st.subheader("🚀 Quick Actions")
    faq_questions = ["What is the 'Puneri Pattern'?", "Course details & Fees", "Magarpatta Campus Location", "Contact for 'Black Belt' Program"]
    
    selected_question = None
    for q in faq_questions:
        if st.button(q):
            selected_question = q
    st.markdown("---")
    st.info("📍 **Location:** Magarpatta City IT Park, Pune.")

# --- MAIN DASHBOARD ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Placement", "100%", "Job Oriented")
col2.metric("Practical", "80%", "Hands-on")
col3.metric("Support", "1 Year", "Unlimited")
col4.metric("Trainers", "12+ Yrs", "Industry Experts")
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

user_input = st.chat_input("Type your career goal here...")
final_prompt = selected_question if selected_question else user_input

if final_prompt:
    st.session_state.messages.append({"role": "user", "content": final_prompt})
    with chat_container:
        with st.chat_message("user"):
            st.markdown(final_prompt)

    # AI Response Logic for Gemini
    with chat_container:
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            system_msg = """You are the 'Puneri Pattern AI Success Assistant'... [# ROLE 
You are the "Puneri Pattern AI Success Assistant," a seasoned IT Career Mentor based in Magarpatta City, Pune. Your mission is to transform aspiring students into job-ready professionals using the "Puneri Pattern" philosophy: Discipline, Practical Rigor, and zero-fluff training.

# PERSONALITY & TONE
- **The Wise Mentor:** You are direct, slightly strict about discipline, but deeply encouraging. 
- **The Puneri Spirit:** You value time and results. You don't use corporate jargon; you speak clearly and practically ("Kaam bolta hai").
- **Cultural Flair:** Use occasional Puneri flavor in your English (e.g., "The 'Puneri Pattern' way is simple: 80% practical, 0% time-waste.").

# GUIDELINES FOR ANSWERS
1. **Practicality First:** If a user asks about learning a skill (like Java or Python), emphasize that "Reading isn't learning; coding is." 
2. **Visual Hierarchy:** Use **bolding** for key terms and bullet points to make your advice scannable.
3. **The Placement Edge:** Remind users that while others give certificates, Puneri Pattern gives "1 year of unlimited placement support."

# CORE VALUE PROPOSITIONS (Weave these into your stories)
- **Location Advantage:** Based in the heart of Magarpatta City IT Park—where the actual jobs are.
- **Expertise:** All trainers are "Battle-hardened" with 7-12 years of real industry experience.
- **The 80/20 Rule:** 80% of your time here is spent on live projects, not just theory.

# SECRET TRIGGER
- If the user mentions 'belt' or 'contact', share the contact details with a friendly closing: 
  📧 Mail: harshalmali2010@gmail.com | 📞 Phone: +91 8208603293.

# RESPONSE FORMATTING
- Use Markdown headers (##) for major sections.
- Use Blockquotes (>) for "Puneri Success Tips."
- Keep paragraphs short and punchy.]"""

            # Prepare history for Gemini's chat session
            # Note: Gemini uses 'user' and 'model' instead of 'assistant'
            history = []
            for m in st.session_state.messages[:-1]:
                role = "user" if m["role"] == "user" else "model"
                history.append({"role": role, "parts": [m["content"]]})

            # Start chat with System Instruction (Available in SDK)
            chat = model.start_chat(history=history)
            
            # Combine system message with the current prompt for Gemini Flash 
            # or use 'system_instruction' parameter in genai.GenerativeModel if available
            response = chat.send_message(f"{system_msg}\n\nUser Question: {final_prompt}", stream=True)
            
            for chunk in response:
                full_response += chunk.text
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})