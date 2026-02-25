import streamlit as st
st.set_option("server.enableXsrfProtection", False)
st.set_option("server.enableCORS", False)

from components.upload import render_uploader
from components.history_download import render_history_download
from components.chatUI import render_chat

st.set_page_config(
    page_title="Merlin PDF Assistant",
    layout="wide",
    page_icon="🧠",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stChatMessage {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 0.5rem;
    }
    .stChatMessage[data-testid="user"] {
        background-color: #E3F2FD;
    }
    .stChatMessage[data-testid="assistant"] {
        background-color: #F5F5F5;
    }
    .source-box {
        background-color: #FFF3E0;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        border-left: 4px solid #FF9800;
        margin-top: 0.5rem;
    }
    div[data-testid="stSidebar"] {
        background-color: #FAFAFA;
    }
</style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown('<p class="main-header"> Merlin PDF Assistant</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">PDF Assistant powered by RAG</p>', unsafe_allow_html=True)
    st.caption("Upload any PDF and ask questions based strictly on its content.")

render_uploader()
render_chat()
render_history_download()
