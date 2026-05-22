import streamlit as st
import random

# Set up page config
st.set_page_config(page_title="Cyber Scramble", page_icon="💾", layout="centered")

# --- WORDS DATABASE ---
WORDS_DB = {
    "STREAMLIT": "A framework to turn python scripts into web apps.",
    "PYTHON": "The programming language you are using right now.",
    "ALGORITHM": "A step-by-step procedure for solving a problem.",
    "VARIABLE": "A storage location paired with an associated symbolic name.",
    "COMPILER": "Translates high-level source code into machine language.",
    "DATABASE": "An organized collection of structured information or data."
}

# --- CUSTOM HTML/CSS STYLING ---
st.markdown("""
    <style>
    /* Global background/font tweaks for terminal feel */
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&display=swap');
    
    .stApp {
        background-color: #0d1117;
    }
    
    .terminal-header {
        text-align: center;
        color: #00ff66;
        font-family: 'Fira Code', monospace;
        text-shadow: 0 0 10px #00ff66;
        margin-bottom: 5px;
    }
    
    .scrambled-box {
        background-color: #161b22;
        border: 2px solid #00ff66;
        box-shadow: 0 0 15px rgba(0, 255, 102, 0.2);
        padding: 20px;
        border-radius: 8px;
        text-align: center;
        font-size: 2.5rem;
        font-family: 'Fira Code', monospace;
        letter-spacing: 8px;
        color: #00ff66;
        margin: 20px 0;
    }
    
    .hint-text {
        font-family: 'Fira Code', monospace;
        color: #8b949e;
        background: #21262d;
        padding: 10px;
        border-left: 4px solid #58a6ff;
        border-radius: 4px;
    }
    
    /* Dynamic Health Bar Wrapper */
    .health-bar-container {
        width: 100%;
        background-color: #30363d;
        border-radius: 10px;
        margin: 15px 0;
    }
    </style>
""", unsafe_allow_html=True)

# --- GAME LOGIC FUNCTIONS ---
def start_new_game():
    word = random.choice(list(WORDS_DB.keys()))
    scrambled = list(word)
    # Ensure it's actually scrambled
    while "".join(scrambled) == word:
        random.shuffle(scrambled)
        
    st.session_state.secret_word = word
    st.session_state.scrambled_word = "".join(scrambled)
    st.session_state.hint = WORDS_DB[word]
    st.session_state.attempts_left = 5
    st.session_state.game_over = False
    st.session_state.won = False

# --- STATE MANAGEMENT ---
if 'secret_word' not in st.session_state:
    start_new_game()

# --- HTML INTERACTIVE COMPONENTS ---
st.markdown("<h1 class='terminal-header'>⚡ DECRYPT THE WORD ⚡</h1>", unsafe_allow_html=True)

# Generate HTML Health Bar dynamically based on python state
health_percentage = (st.session_state.attempts_left / 5) * 100
bar_color = "#00ff66" if st.session_state.attempts_left > 2 else "#ff3333"

st.markdown(f"""
    <div style="font-family: 'Fira Code', monospace; color: white; font-size: 0.9rem;">
        SYSTEM INTEGRITY: {st.session_state.attempts_left}/5 TRIES LEFT
    </div>
    <div class="health-bar-container">
        <div style="width: {health_percentage}%; background-color: {bar_color}; height: 12px; border-radius: 10px; transition: width 0.5s ease;"></div>
    </div>
""", unsafe_allow_html=True)

# Display Scrambled Word Box
st.markdown(f"<div class='scrambled-box'>{st.session_state.scrambled_word}</div>", unsafe_allow_html=True)

# Display Hint via HTML markup
st.markdown(f"<div class='hint-text'><strong>🔍 SYSTEM HINT:</strong> {st.session_state.hint}</div>", unsafe_allow_html=True)
st.write("") # Spacer

# --- USER INPUT & EVALUATION ---
if not st.session_state.game_over:
    # Form forces user to hit Enter or click submit before processing
    with st.form(key="guess_form", clear_on_submit=True):
        user_guess = st.text_input("Enter your decryption guess:", placeholder="Type here...").strip().upper()
        submit_button = st.form_submit_button(label="🚀 SUBMIT CODE")
        
    if submit_button:
        if user_guess == st.session_state.secret_word:
            st.session_state.won = True
            st.session_state.game_over = True
            st.rerun()
        else:
            st.session_state.attempts_left -= 1
            if st.session_state.attempts_left <= 0:
                st.session_state.game_over = True
            st.rerun()

# --- WIN / LOSS STATES ---
if st.session_state.game_over:
    if st.session_state.won:
        st.success(f"🔓 ACCESS GRANTED! You correctly decrypted: {st.session_state.secret_word}")
        st.balloons()
    else:
        st.error(f"🔒 SYSTEM LOCKED! The correct word was: {st.session_state.secret_word}")
    
    # New Game Button
    if st.button("🔄 Initialize Next Override (Play Again)"):
        start_new_game()
        st.rerun()
