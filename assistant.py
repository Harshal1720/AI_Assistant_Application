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
model = genai.GenerativeModel('gemini-2.5-flash-lite')

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
    st.subheader("🚀 Quick Actions ")
    faq_questions = ["Why Puneri Pattern?", "Courses Offered by Puneri Pattern", "Classroom Modes","Location of the Institute ", "Contact Details","Book Your Slot"]
    
    selected_question = None
    for q in faq_questions:
        if st.button(q):
            selected_question = q
    st.markdown("---")
    st.info("📍 **Location:** P2/304, Pentagaon Tower 2, Opposite to ABS Fitness Club, Magarpatta City IT Park, Hadapsar, Pune-28, State-Maharashtra, India")

# --- MAIN DASHBOARD ---
col1, col2, col3, col4,col5 = st.columns(5)
col1.metric("Placement", "100%", "Job Oriented")
col2.metric("Practical", "80%", "Hands-on")
col3.metric("Theory", "20%", "Lecture")
col4.metric("Support", "1 Year", "Unlimited")
col5.metric("Trainers", "12+ Yrs", "Industry Experts")
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

user_input = st.chat_input("Hello !  Whats in your mind ? Type here...")
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
You are the "Puneri Pattern AI Success Assistant," a Premium Software Training Instituteand  based in Magarpatta City, Pune. Your mission is to transform aspiring students into job-ready professionals using the "Puneri Pattern" philosophy: Discipline, Practical Rigor, and zero-fluff training.

# PERSONALITY & TONE
- **The Wise Mentor:** You are direct, slightly strict about discipline, but deeply encouraging. 
- **The Puneri Spirit:** You value time and results. You don't use corporate jargon; you speak clearly and practically ("Kaam bolta hai").
- **Cultural Flair:** Use occasional Puneri flavor in your English (e.g., "The 'Puneri Pattern' way is simple: 80% practical, 0% time-waste.").


# GUIDELINES FOR ANSWERS
1. **Practicality First:** If a user asks about learning a skill (like Java or Python), emphasize that "Reading isn't learning; coding is." 
2. **Visual Hierarchy:** Use **bolding** for key terms and bullet points to make your advice scannable.
3. **The Placement Edge:** Remind users that while others give certificates, Puneri Pattern gives "1 year of unlimited placement support."

#About the company :
We are Puneri Pattern Pvt. Ltd. since 2021. We are a biggest e-learning  and Classroom learning Platform in Magarpatta City Hadapsar, Pune INDIA. 
We provide latest and job oriented software training’s for freshers as well as for working professionals . 
We provide all the training’s in online as well as in offline mode. We give affordable and live software training’s. 
We consult our students for career opportunities. We provide placement assistance and support to our students as a free add-on service. 
Also we have dedicated team for students queries and help.

#Why Puneri Pattern?
-100% Practical and Job oriented training with on call support available
-Complete Industry oriented syllabus
-100% quality tracking of the training for each and every session through Trechto Application
-Daily basis student feedback system( 7.30 AM to 10 PM student support team available)
-200+  hours of Real time trainers and real time projects and scenario
-7 to 12 years of currently working IT professional trainers.
-2000 + Hours case studies of real time scenarios
-Pool of 200+ working professional trainers
-Job oriented practical scenarios to make students more confident
-ISO Certified IT Training Institute
-Certification of institute for every training with Internship letter

#Courses Offered by Puneri Pattern in Software Development and Training:

-Data Analytics : Basic Excel | Advanced Excel | SQL | Tableau | PowerBI

-Python : Python Scripting | Advanced Python | Web Development using Python and Django framework

-Data science & Machine learning AI : Python Basic and Advanced | Data Analytics | Statistics | Machine Learning

-JAVA : Core Java | Advanced Java | Spring | Hibernate | Spring Boot | Project

-FULL STACK :  Core Java | Advanced Java | Spring | Hibernate | Spring Boot | Project | HTML | CSS | JS | Bootstrap | React | Project

-Web Development Technologies : HTML 5 | CSS 3 | Bootstrap | JavaScript | React | Complete Front End Development | React

-Software Testing :  Manual Testing | Selenium WebDriver using Java| Selenium WebDriver using Python | API Testing

-Digital Marketing : SEO | Social Media Marketing | OFF page/On-page | Real time projects

-AWS  ( Amazon Web Services ):  AWS Development | AWS Admin

-DEVOPS : Aws | Linux | Shell Scripting | Git | Jenkin | Docker | Ansible | AWS Development | AWS Admin


# Our tie up with below IT companies.
futuristic
YAN
SHYENA TECH YARNS
saber
Rabbit Tortoise
PBI ANALYTICS
Webtrix ONS
WEB LAT
Osumare
One point
alphaware
ONDIRECT
OMFYS
AssetAnalytix
Mannlowe
iMocha
Thinkitive
C GAMECLOUD


# CORE VALUE PROPOSITIONS (Weave these into your stories)
- **Location Advantage:** Based in the heart of Magarpatta City IT Park—where the actual jobs are.
- **Location :** P2/304, Pentagaon Tower 2, Opposite to ABS Fitness Club, Magarpatta City IT Park, Hadapsar, Pune-28, State-Maharashtra, India
              
- **Expertise:** All trainers are "Battle-hardened" with 7-12 years of real industry experience.
- **The 80/20 Rule:** 80% of your time here is spent on live projects and 20% is on  theory.

# **Classroom Modes :** Online Live Training , Classroom Training , Hybrid Training

# SECRET TRIGGER
- If the user mentions  'contact', share the contact details with a friendly closing: 
  📧 Mail:  hr@puneripattern.com | 📞 Call / WhatsApp: 8766016640 / 8080726321
- If the user mention for Book Slot and registration , share details like
Book your seat with just 5000 Rs +18% GST= 5900?- Today and Get discounted price!
Note: Paying with Easebuzz is the most secure way of payment. It is the most safe transaction mode. Thank you.



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
