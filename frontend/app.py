import streamlit as st
import requests
import time
from utils.docx_exporter import create_draft_docx

# Configure the Streamlit app's presentation
st.set_page_config(page_title="CSR to Article Generator", page_icon="🧬", layout="wide")

# CSS to make the alert prominent
st.markdown("""
<style>
    .draft-alert {
        padding: 1rem;
        background-color: #ffcccc;
        color: #990000;
        border-left: 5px solid #ff0000;
        border-radius: 4px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Application Header
st.title("🧬 CSR to Research Article Draft")
st.markdown("Accelerate scientific writing by extracting and structuring Clinical Study Reports into publication-ready, IMRaD drafts.")

st.markdown('<div class="draft-alert">⚠️ DRAFT – FOR HUMAN REVIEW ONLY. Not a final submission.</div>', unsafe_allow_html=True)

# State initialization
if "imrad_data" not in st.session_state:
    st.session_state.imrad_data = None
if "edited_sections" not in st.session_state:
    st.session_state.edited_sections = {}

# Backend API endpoint configuration
#API_URL = "http://127.0.0.1:8000/api/generate-article"
API_URL = "https://csr-backend-jkj2.onrender.com/api/generate-article"
# Sidebar for file upload
with st.sidebar:
    st.header("Upload Document")
    uploaded_file = st.file_uploader("Upload CSR (PDF or DOCX)", type=['pdf', 'docx'])
    
    generate_btn = st.button("Generate Research Article Draft", type="primary", use_container_width=True, disabled=not uploaded_file)
    
    if generate_btn and uploaded_file:
        with st.spinner("Analyzing document and generating draft..."):
            try:
                # Send the file to the FastAPI backend
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                response = requests.post(API_URL, files=files, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("status") == "success":
                        st.session_state.imrad_data = data.get("data")
                        st.session_state.edited_sections = data.get("data").copy()
                        st.success("Draft generated successfully!")
                    else:
                        st.error("Failed to generate draft. Unexpected response format.")
                else:
                    st.error(f"Backend Error: {response.status_code} - {response.text}")
                    
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to the backend API: {e}")

# Main body: Tabbed interface for editing
if st.session_state.imrad_data:
    st.header("Review and Edit Draft")
    
    tabs = st.tabs(["Abstract", "Introduction", "Methods", "Results", "Discussion"])
    
    sections = ["Abstract", "Introduction", "Methods", "Results", "Discussion"]
    
    # Render text areas within tabs
    for idx, tab in enumerate(tabs):
        section_name = sections[idx]
        with tab:
            st.markdown(f"**Editable {section_name}**")
            # Bind the text area back to session state to save manual edits
            new_text = st.text_area(
                "Edit content below:", 
                value=st.session_state.edited_sections.get(section_name, ""), 
                height=300, 
                key=f"text_area_{section_name}"
            )
            st.session_state.edited_sections[section_name] = new_text

    st.markdown("---")
    st.subheader("Export")
    st.markdown("Download your reviewed and edited draft as a Microsoft Word document.")
    
    # Generate DOCX and offer download
    docx_buffer = create_draft_docx(st.session_state.edited_sections)
    st.download_button(
        label="📄 Download Draft as DOCX",
        data=docx_buffer,
        file_name="Research_Article_Draft.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        type="primary"
    )
else:
    st.info("Upload a Clinical Study Report and click 'Generate' to see the draft here.")
