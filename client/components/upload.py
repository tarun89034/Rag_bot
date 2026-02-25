import streamlit as st
from utils.api import upload_pdfs_api
import time

def render_uploader():
    with st.sidebar:
        st.markdown("### 📄 Upload Documents")
        st.markdown("---")
        
        uploaded_files = st.file_uploader(
            "Upload medical PDF documents",
            type="pdf",
            accept_multiple_files=True,
            help="Upload one or more PDF files to add to the knowledge base"
        )
        
        if uploaded_files:
            st.info(f"📁 {len(uploaded_files)} file(s) selected")
            for f in uploaded_files:
                st.markdown(f"- {f.name}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            upload_btn = st.button("📤 Upload to DB", use_container_width=True)
        
        with col2:
            clear_btn = st.button("🗑️ Clear Chat", use_container_width=True)
        
        if upload_btn and uploaded_files:
            with st.spinner("Processing documents..."):
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)
                    progress_bar.progress(i + 1)
                
                response = upload_pdfs_api(uploaded_files)
                
                if response.status_code == 200:
                    st.success("✅ Documents uploaded successfully!")
                    st.balloons()
                else:
                    st.error(f"❌ Error: {response.text}")
        
        if clear_btn:
            if "messages" in st.session_state:
                st.session_state.messages = []
            if "sources" in st.session_state:
                st.session_state.sources = {}
            st.rerun()
        
        st.markdown("---")
        st.markdown("""
        ### ℹ️ How to use
        1. Upload PDF documents
        2. Click "Upload to DB"
        3. Ask questions in the chat
        4. Get AI-powered answers
        """)
        
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #888; font-size: 0.8rem;">
            Powered by LLaMA3 & Pinecone
        </div>
        """, unsafe_allow_html=True)
