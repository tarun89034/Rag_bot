import streamlit as st
import requests
from config import API_URL
import time

def render_uploader():
    with st.sidebar:
        st.markdown("### 📄 Upload Documents")
        st.markdown("---")
        
        # Option 1: Upload via URL (bypasses Streamlit entirely)
        pdf_url = st.text_input("Enter PDF URL", placeholder="https://example.com/document.pdf")
        
        if pdf_url:
            st.info(f"📎 URL: {pdf_url}")
        
        # Option 2: Small file upload (for testing)
        with st.expander("Or upload small files"):
            uploaded_files = st.file_uploader(
                "Choose PDF files",
                type="pdf",
                accept_multiple_files=True
            )
            if uploaded_files:
                st.info(f"📁 {len(uploaded_files)} file(s)")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            upload_url_btn = st.button("📥 Load from URL", use_container_width=True)
        
        with col2:
            upload_file_btn = st.button("📤 Upload Files", use_container_width=True)
        
        with col3:
            clear_btn = st.button("🗑️ Clear Chat", use_container_width=True)
        
        # Handle URL upload
        if upload_url_btn and pdf_url:
            with st.spinner("Downloading and processing..."):
                try:
                    response = requests.post(
                        f"{API_URL}/upload_from_url/",
                        json={"url": pdf_url},
                        timeout=300
                    )
                    if response.status_code == 200:
                        st.success("✅ Document loaded successfully!")
                        st.balloons()
                    else:
                        st.error(f"❌ Error: {response.text}")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        
        # Handle file upload
        if upload_file_btn and uploaded_files:
            with st.spinner("Processing documents..."):
                try:
                    pdf_files = [("files", (f.name, f.getvalue(), "application/pdf")) for f in uploaded_files]
                    response = requests.post(
                        f"{API_URL}/upload_pdfs/",
                        files=pdf_files,
                        timeout=300
                    )
                    if response.status_code == 200:
                        st.success("✅ Documents uploaded successfully!")
                        st.balloons()
                    else:
                        st.error(f"❌ Error: {response.text}")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        
        if clear_btn:
            if "messages" in st.session_state:
                st.session_state.messages = []
            if "sources" in st.session_state:
                st.session_state.sources = {}
            st.rerun()
        
        st.markdown("---")
        st.markdown("""
        ### ℹ️ How to use
        1. Enter PDF URL or upload files
        2. Click "Load from URL" or "Upload Files"
        3. Ask questions in the chat
        4. Get AI-powered answers
        """)
        
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #888; font-size: 0.8rem;">
            Powered by LLaMA3 & Pinecone
        </div>
        """, unsafe_allow_html=True)
