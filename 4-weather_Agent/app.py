import streamlit as st
from prompts import build_greeting_prompt
from agent import run_agent_turns

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="🌤️ Weather Agent",
    page_icon="🌤️",
    layout="centered",
)

# ── Custom styling ───────────────────────────────────────────
st.markdown("""
<style>
    /* Main header gradient */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2rem;
        font-weight: 700;
    }
    .main-header p {
        color: rgba(255,255,255,0.85);
        margin: 0.3rem 0 0 0;
        font-size: 0.95rem;
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    section[data-testid="stSidebar"] * {
        color: #e0e0e0 !important;
    }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #a78bfa !important;
    }

    /* Chat message styling */
    .stChatMessage {
        border-radius: 12px;
        margin-bottom: 0.5rem;
    }

    /* Input box */
    .stChatInput > div {
        border-radius: 12px;
    }

    /* Suggestion chips */
    .suggestion-chip {
        display: inline-block;
        background: linear-gradient(135deg, #667eea22, #764ba222);
        border: 1px solid #667eea44;
        border-radius: 20px;
        padding: 0.4rem 1rem;
        margin: 0.25rem;
        font-size: 0.85rem;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    /* Status indicator */
    .status-dot {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #4ade80;
        margin-right: 6px;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.4; }
    }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌦️ About")
    st.markdown(build_greeting_prompt())
    
    st.divider()
    
    st.markdown("### ⚙️ Info")
    st.markdown(
        '<p><span class="status-dot"></span> Open-Meteo API (Free, no key needed)</p>',
        unsafe_allow_html=True,
    )
    st.markdown("- 🌡️ Temperature in °C")
    st.markdown("- 💨 Wind speed in km/h")
    st.markdown("- 🌤️ Live sky conditions")
    
    st.divider()
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ── Header ───────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🌤️ Weather Agent</h1>
    <p>Ask me about live weather anywhere in the world</p>
</div>
""", unsafe_allow_html=True)

# ── Session state ────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_input" not in st.session_state:
    st.session_state.pending_input = None

# ── Display chat history ─────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🌤️" if msg["role"] == "assistant" else "🧑"):
        st.markdown(msg["content"])

# ── Show suggestions if no messages yet ──────────────────────
if not st.session_state.messages:
    st.markdown("#### 💡 Try asking:")

    suggestions = [
        "What is the weather like in Lucknow?",
        "What is the temperature in New York?",
        "What is the windspeed in Tokyo?",
        "Compare weather of Lucknow and New York?",
    ]

    cols = st.columns(2)
    for i, suggestion in enumerate(suggestions):
        with cols[i % 2]:
            if st.button(f"🔹 {suggestion}", key=f"sug_{i}", use_container_width=True):
                st.session_state.pending_input = suggestion
                st.rerun()

# ── Determine user input (typed or suggestion) ───────────────
user_input = st.chat_input("Ask about the weather...") or st.session_state.pending_input
if st.session_state.pending_input:
    st.session_state.pending_input = None  # clear after consuming

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display user message
    with st.chat_message("user", avatar="🧑"):
        st.markdown(user_input)

    # Get agent response
    with st.chat_message("assistant", avatar="🌤️"):
        with st.spinner("🔍 Fetching live weather data..."):
            agent_messages = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]
            response = run_agent_turns(agent_messages)

        st.markdown(response)

    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})

