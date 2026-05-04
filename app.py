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

# --- FUN, NEON PINK & PURPLE SPACE THEME ---
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Deep Space Purple Background */
    .stApp {
        background-color: #1a0b2e;
        background-image: radial-gradient(circle at 50% 10%, #3a0ca3 0%, #1a0b2e 80%);
        color: #ffffff;
    }

    /* Tabs Styling - Bubbly and Fun */
    div[data-testid="stTabs"] > div > div > div { overflow: visible !important; }
    div[data-baseweb="tab_list"] {
        background-color: rgba(45, 27, 78, 0.8);
        border-radius: 25px;
        padding: 10px;
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 10px;
        margin-bottom: 2rem;
        border: 2px solid #7209b7;
    }
    button[data-baseweb="tab"] {
        background-color: transparent !important;
        border: none !important;
        padding: 12px 18px !important;
    }
    button[data-baseweb="tab"] p {
        color: #e2e8f0 !important;
        font-size: 1.05rem !important;
        font-weight: 700 !important;
    }
    /* Active Tab - Bright Pink Glow */
    button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #f72585 !important;
        border-radius: 15px !important;
        box-shadow: 0 0 15px rgba(247, 37, 133, 0.6) !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] p {
        color: #ffffff !important; 
        font-weight: 900 !important;
    }

    /* Hero Section */
    .hero-title {
        font-size: 3.8rem;
        font-weight: 900;
        text-align: center;
        color: #ffffff;
        margin-bottom: 0.2rem;
        text-shadow: 0 0 10px rgba(247, 37, 133, 0.5);
    }
    .hero-title span { color: #f72585; }
    .hero-subtitle {
        text-align: center;
        font-size: 1.3rem;
        color: #f1a5ff;
        margin-bottom: 2.5rem;
        font-weight: 700;
    }

    /* ---------------------------------------------------
       INPUTS - HIGH CONTRAST & VISIBILITY FIX
       --------------------------------------------------- */
    
    .stTextInput label p, .stNumberInput label p, .stTextArea label p {
        color: #f1a5ff !important; 
        font-size: 1.15rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.5px;
    }

    .stTextInput input, .stTextArea textarea, .stNumberInput input {
        background-color: #2d1b4e !important;
        color: #ffffff !important; 
        border: 3px solid #b5179e !important;
        border-radius: 15px !important;
        font-size: 1.2rem !important;
        padding: 12px !important;
        font-weight: bold !important;
    }

    .stTextInput input::placeholder, .stTextArea textarea::placeholder {
        color: #d8b4e2 !important; 
        opacity: 0.8 !important;
    }

    .stTextInput input:focus, .stTextArea textarea:focus, .stNumberInput input:focus {
        border-color: #f72585 !important;
        box-shadow: 0 0 15px rgba(247, 37, 133, 0.5) !important;
    }

    /* Buttons - Bright Gradients */
    div.stButton > button {
        background: linear-gradient(90deg, #7209b7 0%, #f72585 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 50px !important;
        width: 100% !important;
        padding: 1.2rem !important;
        font-size: 1.3rem !important;
        font-weight: 900 !important;
        letter-spacing: 1px !important;
        transition: transform 0.2s, box-shadow 0.2s;
        box-shadow: 0 4px 15px rgba(114, 9, 183, 0.4) !important;
    }
    div.stButton > button:hover {
        transform: scale(1.03) !important;
        box-shadow: 0 0 20px rgba(247, 37, 133, 0.8) !important;
    }

    /* Formatting AI Output & Boxes */
    .stMarkdown h2, .stMarkdown h3 { color: #f1a5ff !important; font-weight: 800 !important; }
    .stMarkdown p, .stMarkdown li { font-size: 1.2rem; line-height: 1.6; color: #f8fafc !important; }
    
    .question-box {
        background: linear-gradient(135deg, #3a0ca3, #7209b7);
        padding: 25px;
        border-radius: 20px;
        border: 3px solid #f72585;
        margin-bottom: 20px;
        font-size: 1.4rem;
        font-weight: 900;
        color: white;
        text-align: center;
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
    }
    .score-box {
        text-align: center;
        font-size: 2.5rem;
        color: #f72585;
        font-weight: 900;
        margin-bottom: 20px;
        text-shadow: 0 0 15px rgba(247, 37, 133, 0.4);
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

# Daily Challenge Generator
def generate_daily_quiz():
    quiz = []
    ops = ['+', '-', 'x', '÷']
    for _ in range(10):
        op = random.choice(ops)
        if op == '+':
            a, b = random.randint(15, 200), random.randint(15, 200)
            ans = a + b
        elif op == '-':
            a, b = random.randint(50, 300), random.randint(10, 49)
            ans = a - b
        elif op == 'x':
            a, b = random.randint(3, 12), random.randint(3, 12)
            ans = a * b
        elif op == '÷':
            b = random.randint(2, 12)
            ans = random.randint(2, 12)
            a = b * ans 
        quiz.append({'q': f"{a} {op} {b}", 'ans': ans})
    return quiz

if 'daily_quiz' not in st.session_state:
    st.session_state.daily_quiz = generate_daily_quiz()
    st.session_state.quiz_submitted = False

if not st.session_state.meteor_q:
    generate_meteor()

# --- APP LAYOUT ---
st.markdown("<div class='hero-title'>Cosmic <span>Math</span> 🚀</div>", unsafe_allow_html=True)
st.markdown("<div class='hero-subtitle'>Your Epic Math Universe!</div>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📚 Learn", "🎯 Practice", "🏆 10-Q Challenge", "✖️ Tables", "🕹️ Arcade", "🦄 Story Math"])

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
            prompt = f"You are a fun, interactive math teacher. Explain '{concept_input}'. Use 3 simple steps, a fun everyday example, and emojis. Do not sound like a boring textbook."
            with st.spinner("Firing up the learning rockets... 🚀"):
                response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}])
                st.markdown(response.choices[0].message.content)

# ==========================================
# TAB 2: PRACTICE MISSION (Custom Topic)
# ==========================================
with tab2:
    st.write("### Focus on one special topic!")
    practice_topic = st.text_input("What topic should we practice? (e.g., Multiplying by 10)", key="practice_topic")
    
    if st.button("Give Me a Mission! 🎲"):
        if not practice_topic.strip():
            st.error("Please pick a topic first!")
        else:
            api_key = os.getenv("GROQ_API_KEY")
            client = Groq(api_key=api_key)
            prompt = f"Generate ONE fun math word problem about: {practice_topic}. Ask the question only. Do not give the answer."
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
                check_prompt = f"Question: {st.session_state.current_question}. Student Answer: {student_answer}. Be extremely encouraging! Tell the student if they are right or wrong, then explain step-by-step how to solve it."
                with st.spinner("Checking your math... 🧮"):
                    response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": check_prompt}])
                    st.markdown("---")
                    st.markdown(response.choices[0].message.content)
                    if st.button("Clear and Start New Mission"):
                        st.session_state.current_question = ""
                        st.rerun()

# ==========================================
# TAB 3: 10-QUESTION DAILY CHALLENGE
# ==========================================
with tab3:
    st.write("### 🏆 The 10-Question Daily Challenge!")
    st.write("A brand new mix of addition, subtraction, multiplication, and division every time you open the app!")
    
    quiz_answers = []
    for i, q in enumerate(st.session_state.daily_quiz):
        st.markdown(f"**Question {i+1}:**")
        ans = st.number_input(f"{q['q']} = ?", key=f"quiz_q_{i}", value=0, step=1)
        quiz_answers.append(ans)
        st.markdown("---")

    if st.button("Submit My Quiz! 🚀"):
        score = 0
        mistakes_for_ai = []
        
        st.write("### Let's see how you did!")
        
        for i, q in enumerate(st.session_state.daily_quiz):
            user_ans = quiz_answers[i]
            correct_ans = q['ans']
            if user_ans == correct_ans:
                score += 1
                st.success(f"**Q{i+1}:** {q['q']} = {user_ans} ✅ **Correct!**")
            else:
                st.error(f"**Q{i+1}:** {q['q']} = {user_ans} ❌ *(Correct answer: {correct_ans})*")
                mistakes_for_ai.append(f"{q['q']} (Student guessed {user_ans})")
        
        st.markdown(f"<div class='score-box'>Your Score: {score}/10</div>", unsafe_allow_html=True)
        
        if score == 10:
            st.balloons()
            st.success("🎉 PERFECT SCORE! You are a Math Genius! 🎉")
        
        api_key = os.getenv("GROQ_API_KEY")
        client = Groq(api_key=api_key)
        
        if score < 10:
            prompt = f"""You are a fun, engaging math teacher. A student just took a 10-question math quiz and got {score}/10. 
            They made mistakes on these specific problems: {mistakes_for_ai}.
            Write a very encouraging message congratulating them on the ones they got right. 
            Then, provide a simple, step-by-step explanation ONLY for the problems they got wrong. Use lots of emojis!"""
        else:
             prompt = "A student just got a perfect 10/10 on their daily math mix. Write a short, extremely hype, congratulatory message with lots of space/rocket emojis!"
             
        with st.spinner("AI Teacher is writing your feedback... ✍️"):
            response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}])
            st.markdown("### 👩‍🏫 Teacher's Notes:")
            st.markdown(response.choices[0].message.content)

    if st.button("🔄 Generate a Brand New 10-Question Quiz!"):
        st.session_state.daily_quiz = generate_daily_quiz()
        st.rerun()

# ==========================================
# TAB 4: TIMES TABLE TURBO
# ==========================================
with tab4:
    st.write("### Master Your Multiplication Tables!")
    st.write("Pick a number to see its table and unlock a magic memory trick.")
    
    table_num = st.slider("Select a number:", 1, 20, 7)
    
    cols = st.columns(3)
    for i in range(1, 21):
        col_index = (i - 1) % 3
        cols[col_index].markdown(f"**{table_num} x {i} = {table_num * i}**")
        
    st.markdown("---")
    if st.button(f"Show me a Magic Trick for the {table_num}s Table! ✨"):
        api_key = os.getenv("GROQ_API_KEY")
        client = Groq(api_key=api_key)
        prompt = f"I am a student. Teach me a fun memory trick, pattern, or rhyme to help me memorize the multiplication table for the number {table_num} (up to {table_num} x 20). Make it super fun and easy!"
        with st.spinner("Asking the AI Math Wizard... 🧙‍♂️"):
            response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}])
            st.markdown(response.choices[0].message.content)

# ==========================================
# TAB 5: MATH ARCADE (METEOR DEFENSE)
# ==========================================
with tab5:
    st.write("### ☄️ Meteor Defense!")
    st.write("Solve the math problem to fire your lasers and destroy the meteor!")
    
    st.markdown(f"<div class='score-box'>Score: {st.session_state.arcade_score}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='question-box'>Incoming Meteor: <br> <span style='font-size:3rem; color:#f1a5ff;'>{st.session_state.meteor_q} = ?</span></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        arcade_guess = st.number_input("Enter Answer:", value=0, step=1, key="arcade_input")
        
        if st.button("Fire Laser! 💥"):
            if arcade_guess == st.session_state.meteor_ans:
                st.success("🎯 Direct Hit! +10 Points!")
                st.balloons()
                st.session_state.arcade_score += 10
                generate_meteor()
                st.rerun()
            else:
                st.error(f"Missed! The correct answer was {st.session_state.meteor_ans}. Try the next one!")
                st.session_state.arcade_score -= 5
                generate_meteor()
                st.rerun()

# ==========================================
# TAB 6: STORY MATH
# ==========================================
with tab6:
    st.write("### Let's turn your favorite things into math!")
    interests = st.text_input("What do you love? (e.g., Taylor Swift, Minecraft, Cats)")
    
    if st.button("Make My Math Story! 📖"):
        if not interests.strip():
            st.error("Please tell me what you like!")
        else:
            api_key = os.getenv("GROQ_API_KEY")
            client = Groq(api_key=api_key)
            prompt = f"Create a short, fun math story problem featuring: {interests}. Then, directly underneath, provide the step-by-step solution."
            with st.spinner("Writing your custom story... ✍️"):
                response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}])
                st.markdown(response.choices[0].message.content)