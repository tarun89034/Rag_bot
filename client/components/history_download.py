import streamlit as st
from datetime import datetime

def render_history_download():
    if st.session_state.get("messages"):
        with st.sidebar:
            st.markdown("---")
            st.markdown("### 📥 Export Chat")
            
            messages = st.session_state.messages
            sources = st.session_state.get("sources", {})
            
            chat_text = f"RagBot 2.0 - Chat History\n"
            chat_text += f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            chat_text += "=" * 50 + "\n\n"
            
            for i, msg in enumerate(messages):
                role = "🧑 User" if msg["role"] == "user" else "🤖 Assistant"
                chat_text += f"{role}:\n{msg['content']}\n"
                
                if msg["role"] == "assistant" and i in sources and sources[i]:
                    chat_text += "\nSources:\n"
                    for src in sources[i]:
                        chat_text += f"  - {src}\n"
                
                chat_text += "\n" + "-" * 40 + "\n\n"
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.download_button(
                    label="📝 Download .txt",
                    data=chat_text,
                    file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            with col2:
                import json
                json_data = {
                    "exported": datetime.now().isoformat(),
                    "messages": messages,
                    "sources": {str(k): v for k, v in sources.items()}
                }
                st.download_button(
                    label="📋 Download .json",
                    data=json.dumps(json_data, indent=2),
                    file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )
