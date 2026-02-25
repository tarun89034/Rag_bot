import streamlit as st
from utils.api import ask_question
import time

def render_chat():
    st.markdown("### 💬 Chat with your documents")
    
    st.markdown("""
    <style>
        .chat-container {
            max-height: 500px;
            overflow-y: auto;
            padding: 1rem;
            border-radius: 10px;
            background-color: #FAFAFA;
        }
    </style>
    """, unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "sources" not in st.session_state:
        st.session_state.sources = {}

    chat_container = st.container()
    
    with chat_container:
        for i, msg in enumerate(st.session_state.messages):
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                if msg["role"] == "assistant" and i in st.session_state.sources:
                    sources = st.session_state.sources[i]
                    if sources:
                        with st.expander("📄 View Sources"):
                            for src in sources:
                                st.markdown(f"- `{src}`")

    if prompt := st.chat_input("Ask a question about your documents..."):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("🤔 Thinking...")
            
            response = ask_question(prompt)
            
            if response.status_code == 200:
                data = response.json()
                answer = data["response"]
                sources = data.get("sources", [])
                
                message_placeholder.markdown(answer)
                
                if sources:
                    with st.expander("📄 View Sources"):
                        for src in sources:
                            st.markdown(f"- `{src}`")
                
                st.session_state.messages.append({"role": "assistant", "content": answer})
                st.session_state.sources[len(st.session_state.messages) - 1] = sources
            else:
                message_placeholder.markdown(f"❌ **Error:** {response.text}")
