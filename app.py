"""
Streamlit UI for Conversational Knowledge Bot
"""
import streamlit as st
from dotenv import load_dotenv
from bot_core import DeepSeekBot

load_dotenv()

# Page config
st.set_page_config(
    page_title="Chat bot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize bot
@st.cache_resource
def get_bot():
    return KnowledgeBot()

bot = get_bot()

# Custom CSS
st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 2.5em;
        margin-bottom: 0.5em;
    }
    .subtitle {
        text-align: center;
        color: #888;
        margin-bottom: 2em;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 1em;
        border-radius: 0.5em;
        margin-bottom: 1em;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar - Minimal and Secure
with st.sidebar:
    # Clear Memory button only
    if st.button("🔄 Clear Memory", use_container_width=True):
        bot.clear_memory()
        st.session_state.messages = []
        st.success("✅ Memory cleared!")
        st.rerun()

    st.divider()
    st.subheader("💡 Try These Questions")
    sample_qs = [
        "Who is Elon Musk?",
        "What is artificial intelligence?",
        "Explain machine learning",
        "What is quantum computing?",
        "Who won the Nobel Prize in 2023?"
    ]
    for q in sample_qs:
        if st.button(f"❓ {q}", use_container_width=True):
            st.session_state.input_prompt = q
            st.rerun()

# Main content
st.markdown('<h1 class="main-title">🤖 Chat bot</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">100% FREE Conversational AI with Memory</p>', unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
prompt = st.chat_input("Ask me anything...", key="input_prompt")

if prompt:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):
            # Check for special commands
            response = ""
            
            if prompt.lower().startswith("search:"):
                search_query = prompt[7:].strip()
                st.write(f"🔍 Searching for: **{search_query}**")
                response = bot.search_web(search_query)
            
            elif prompt.lower().startswith("wiki:"):
                wiki_query = prompt[5:].strip()
                st.write(f"📚 Wikipedia search: **{wiki_query}**")
                response = bot.get_wikipedia(wiki_query)
            
            else:
                # Regular chat
                response = bot.chat(prompt)
            
            st.markdown(response)
    
    # Add bot response to history
    st.session_state.messages.append({"role": "assistant", "content": response})
