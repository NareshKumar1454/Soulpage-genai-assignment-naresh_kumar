import streamlit as st
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Try to import bot
try:
    from bot_core import ConversationalKnowledgeBot, create_simple_bot
    IMPORT_SUCCESS = True
except ImportError as e:
    IMPORT_SUCCESS = False
    st.error(f"Import Error: {str(e)}")
    st.info("Trying to install required packages...")

# Page configuration
st.set_page_config(
    page_title="DeepSeek Knowledge Bot",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'bot' not in st.session_state:
    st.session_state.bot = None
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'initialized' not in st.session_state:
    st.session_state.initialized = False

# Sidebar
with st.sidebar:
    st.title("⚙️ DeepSeek Bot")
    
    st.subheader("API Key")
    api_key = st.text_input(
        "OpenRouter API Key",
        type="password",
        value=os.getenv("OPENROUTER_API_KEY", "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"),
        help="Default key provided for testing"
    )
    
    if not IMPORT_SUCCESS:
        st.warning("⚠️ Some packages missing. Click below to install.")
        if st.button("Install Packages"):
            with st.spinner("Installing..."):
                import subprocess
                try:
                    subprocess.run([sys.executable, "-m", "pip", "install", "langchain-core==0.1.0", "langchain==0.0.349", "langchain-community==0.0.10"], check=True)
                    st.success("Packages installed! Please refresh the page.")
                    time.sleep(2)
                    st.rerun()
                except:
                    st.error("Installation failed. Please run: pip install langchain-core==0.1.0 langchain==0.0.349")
    
    st.divider()
    
    if st.button("🚀 Initialize Bot", type="primary"):
        if api_key:
            os.environ["OPENROUTER_API_KEY"] = api_key
            try:
                st.session_state.bot = ConversationalKnowledgeBot()
                st.session_state.messages = []
                st.session_state.initialized = True
                st.success("✅ Bot initialized!")
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"Failed: {str(e)}")
        else:
            st.error("Please enter API key")
    
    if st.button("🔄 Clear Chat"):
        st.session_state.messages = []
        if st.session_state.bot and hasattr(st.session_state.bot, 'memory'):
            st.session_state.bot.memory.clear()
        st.success("Chat cleared!")
        st.rerun()
    
    st.divider()
    st.markdown("### 💡 Sample Questions")
    st.markdown("""
    1. Who is the CEO of OpenAI?
    2. What is AI?
    3. Latest technology news
    4. Explain quantum computing
    """)

# Main content
st.title("🤖 DeepSeek Knowledge Bot")
st.markdown("**100% Free AI Chatbot**")

if not IMPORT_SUCCESS:
    st.error("""
    ### ❌ Required packages not installed
    
    Please run in terminal:
    ```
    pip install langchain-core==0.1.0 langchain==0.0.349 langchain-community==0.0.10
    ```
    
    Then refresh this page.
    """)
else:
    # Status
    col1, col2 = st.columns(2)
    with col1:
        if st.session_state.initialized:
            st.success("✅ Bot Active")
        else:
            st.warning("⚠️ Bot Not Initialized")
    with col2:
        st.info("🆓 Free Tier")
    
    st.divider()
    
    # Display chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if st.session_state.initialized and st.session_state.bot:
        if prompt := st.chat_input("Ask me anything..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = st.session_state.bot.chat(prompt)
                    st.markdown(response)
            
            # Add bot response
            st.session_state.messages.append({"role": "assistant", "content": response})
    elif not st.session_state.initialized:
        st.info("👈 Enter API key and click 'Initialize Bot' in sidebar")