import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import random

load_dotenv()

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Cosmic Math Explorer",
    page_icon="🚀",
    layout="centered"
)

# --- FUN, KID-FRIENDLY SPACE THEME ---
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Deep Space Background */
    .stApp {
        background-color: #0b0c10;
        background-image: radial-gradient(circle at 50% 10%, #1f2833 0%, #0b0c10 70%);
        color: #ffffff;
    }

    /* Tabs Styling - Allow wrapping for 5 tabs */
    div[data-testid="stTabs"] > div > div > div { overflow: visible !important; }
    div[data-baseweb="tab_list"] {
        background-color: #1f2833;
        border-radius: 20px;
        padding: 8px;
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 8px;
        margin-bottom: 2rem;
    }
    button[data-baseweb="tab"] {
        background-color: transparent !important;
        border: none !important;
        padding: 10px 15px !important;
    }
    button[data-baseweb="tab"] p {
        color: #c5c6c7 !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #66fcf1 !important;
        border-radius: 12px !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] p {
        color: #0b0c10 !important; 
        font-weight: 900 !important;
    }

    /* Hero Section */
    .hero-title {
        font-size: 3.5rem;
        font-weight: 900;
        text-align: center;
        color: #ffffff;
        margin-bottom: 0.2rem;
    }
    .hero-title span { color: #66fcf1; }
    .hero-subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #45a29e;
        margin-bottom: 2rem;
        font-weight: 600;
    }

    /* Inputs */
    .stTextInput input, .stTextArea textarea, .stNumberInput input {
        background-color: #1f2833 !important;
        color: #ffffff !important;
        border: 2px solid #45a29e !important;
        border-radius: 12px !important;
        font-size: 1.1rem !important;
        padding: 10px !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus, .stNumberInput input:focus {
        border-color: #66fcf1 !important;
        box-shadow: 0 0 10px rgba(102, 252, 241, 0.4) !important;
    }

    /* Buttons */
    div.stButton > button {
        background: linear-gradient(90deg, #45a29e 0%, #66fcf1 100%) !important;
        color: #0b0c10 !important;
        border: none !important;
        border-radius: 50px !important;
        width: 100% !important;
        padding: 1rem !important;
        font-size: 1.2rem !important;
        font-weight: 800 !important;
        transition: transform 0.2s;
    }
    div.stButton > button:hover {
        transform: scale(1.02) !important;
        box-shadow: 0 0 15px rgba(102, 252, 241, 0.6) !important;
    }

    /* Formatting AI Output */
    .stMarkdown h2, .stMarkdown h3 { color: #66fcf1 !important; }
    .stMarkdown p, .stMarkdown li { font-size: 1.15rem; line-height: 1.6; color: #e0e2e4 !important; }
    
    /* Highlight Boxes */
    .question-box {
        background-color: #1f2833;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #66fcf1;
        margin-bottom: 20px;
        font-size: 1.3rem;
        font-weight: bold;
    }
    .score-box {
        text-align: center;
        font-size: 2rem;
        color: #66fcf1;
        font-weight: 900;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE MEMORY ---
if 'current_question' not in st.session_state: st.session_state.current_question = ""
if 'current_topic' not in st.session_state: st.session_state.current_topic = ""
# Arcade Game Memory
if 'arcade_score' not in st.session_state: st.session_state.arcade_score = 0
if 'meteor_q' not in st.session_state: st.session_state.meteor_q = ""
if 'meteor_ans' not in st.session_state: st.session_state.meteor_ans = 0

def generate_meteor():
    """Generates a random quick math problem for the arcade"""
    ops = ['+', '-', 'x']
    op = random.choice(ops)
    if op == '+':
        a, b = random.randint(10, 100), random.randint(10, 100)
        st.session_state.meteor_ans = a + b
    elif op == '-':
        a, b = random.randint(20, 100), random.randint(1, 20)
        st.session_state.meteor_ans = a - b
    else:
        a, b = random.randint(2, 12), random.randint(2, 12)
        st.session_state.meteor_ans = a * b
    st.session_state.meteor_q = f"{a} {op} {b}"

# Generate first meteor if empty
if not st.session_state.meteor_q:
    generate_meteor()

# --- APP LAYOUT ---
st.markdown("<div class='hero-title'>Cosmic <span>Math</span> 🚀</div>", unsafe_allow_html=True)
st.markdown("<div class='hero-subtitle'>Your 5th Grade Learning Universe!</div>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["📚 Learn", "🎯 Practice", "✖️ Tables", "🕹️ Arcade", "🦄 Story Math"])

# ==========================================
# TAB 1: LEARN A CONCEPT
# ==========================================
with tab1:
    st.write("### What do you want to learn today?")
    concept_input = st.text_input("e.g., Fractions, Decimals, or Geometry", key="learn_input")
    
    if st.button("Teach Me! 🌟"):
        if not concept_input.strip():
            st.error("Please type a math topic first!")
        else:
            api_key = os.getenv("GROQ_API_KEY")
            client = Groq(api_key=api_key)
            prompt = f"You are a fun 5th-grade math teacher. Explain '{concept_input}'. Use 3 simple steps, a fun everyday example, and emojis. Do not sound like a boring textbook."
            with st.spinner("Firing up the learning rockets... 🚀"):
                response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}])
                st.markdown(response.choices[0].message.content)

# ==========================================
# TAB 2: PRACTICE MISSION
# ==========================================
with tab2:
    st.write("### Ready for a math mission?")
    practice_topic = st.text_input("What topic should we practice? (e.g., Multiplying by 10)", key="practice_topic")
    
    if st.button("Give Me a Mission! 🎲"):
        if not practice_topic.strip():
            st.error("Please pick a topic first!")
        else:
            api_key = os.getenv("GROQ_API_KEY")
            client = Groq(api_key=api_key)
            prompt = f"Generate ONE fun 5th-grade math word problem about: {practice_topic}. Ask the question only. Do not give the answer."
            with st.spinner("Generating your mission..."):
                response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}])
                st.session_state.current_question = response.choices[0].message.content

    if st.session_state.current_question:
        st.markdown(f"<div class='question-box'>{st.session_state.current_question}</div>", unsafe_allow_html=True)
        student_answer = st.text_input("Type your answer here:")
        
        if st.button("Check My Answer ✅"):
            if not student_answer.strip():
                st.warning("Don't forget to type your answer!")
            else:
                api_key = os.getenv("GROQ_API_KEY")
                client = Groq(api_key=api_key)
                check_prompt = f"Question: {st.session_state.current_question}. Student Answer: {student_answer}. Be extremely encouraging! Tell her if she is right or wrong, then explain step-by-step how to solve it."
                with st.spinner("Checking your math... 🧮"):
                    response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": check_prompt}])
                    st.markdown("---")
                    st.markdown(response.choices[0].message.content)
                    if st.button("Clear and Start New Mission"):
                        st.session_state.current_question = ""
                        st.rerun()

# ==========================================
# TAB 3: TIMES TABLE TURBO
# ==========================================
with tab3:
    st.write("### Master Your Multiplication Tables!")
    st.write("Pick a number to see its table and unlock a magic memory trick.")
    
    # Slider goes from 1 to 20
    table_num = st.slider("Select a number:", 1, 20, 7)
    
    # Display the table cleanly
    cols = st.columns(3)
    
    # Loop goes up to 20 (range 1 to 21)
    for i in range(1, 21):
        col_index = (i - 1) % 3
        cols[col_index].markdown(f"**{table_num} x {i} = {table_num * i}**")
        
    st.markdown("---")
    if st.button(f"Show me a Magic Trick for the {table_num}s Table! ✨"):
        api_key = os.getenv("GROQ_API_KEY")
        client = Groq(api_key=api_key)
        prompt = f"I am a 5th grader. Teach me a fun memory trick, pattern, or rhyme to help me memorize the multiplication table for the number {table_num} (up to {table_num} x 20). Make it super fun and easy!"
        with st.spinner("Asking the AI Math Wizard... 🧙‍♂️"):
            response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}])
            st.markdown(response.choices[0].message.content)

# ==========================================
# TAB 4: MATH ARCADE (METEOR DEFENSE)
# ==========================================
with tab4:
    st.write("### ☄️ Meteor Defense!")
    st.write("Solve the math problem to fire your lasers and destroy the meteor!")
    
    st.markdown(f"<div class='score-box'>Score: {st.session_state.arcade_score}</div>", unsafe_allow_html=True)
    
    st.markdown(f"<div class='question-box' style='text-align:center;'>Incoming Meteor: <br> <span style='font-size:2.5rem; color:#ec4899;'>{st.session_state.meteor_q} = ?</span></div>", unsafe_allow_html=True)
    
    # Use columns to make the input box smaller
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Step=1 ensures it only accepts whole numbers
        arcade_guess = st.number_input("Enter Answer:", value=0, step=1, key="arcade_input")
        
        if st.button("Fire Laser! 💥"):
            if arcade_guess == st.session_state.meteor_ans:
                st.success("🎯 Direct Hit! +10 Points!")
                st.balloons()
                st.session_state.arcade_score += 10
                generate_meteor() # Create the next problem
                st.rerun() # Refresh the page to show new problem
            else:
                st.error(f"Missed! The correct answer was {st.session_state.meteor_ans}. Try the next one!")
                st.session_state.arcade_score -= 5 # Penalty for missing
                generate_meteor()
                st.rerun()

# ==========================================
# TAB 5: STORY MATH
# ==========================================
with tab5:
    st.write("### Let's turn your favorite things into math!")
    interests = st.text_input("What do you love? (e.g., Taylor Swift, Minecraft, Cats)")
    
    if st.button("Make My Math Story! 📖"):
        if not interests.strip():
            st.error("Please tell me what you like!")
        else:
            api_key = os.getenv("GROQ_API_KEY")
            client = Groq(api_key=api_key)
            prompt = f"Create a short 5th-grade math story problem featuring: {interests}. Then, directly underneath, provide the step-by-step solution."
            with st.spinner("Writing your custom story... ✍️"):
                response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}])
                st.markdown(response.choices[0].message.content)