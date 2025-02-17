import streamlit as st
from utils.text_processor import TextProcessor
from utils.classifier import EmailClassifier

def initialize_session_state():
    if 'text_processor' not in st.session_state:
        st.session_state.text_processor = TextProcessor()
    if 'classifier' not in st.session_state:
        st.session_state.classifier = EmailClassifier()

def get_status_color(classification):
    if classification == "Safe":
        return "#28a745"  # Green
    elif classification == "Spam":
        return "#ffc107"  # Yellow
    else:
        return "#dc3545"  # Red

def main():
    initialize_session_state()

    st.set_page_config(
        page_title="Email Classification System",
        page_icon="✉️",
        layout="wide"
    )

    # Custom CSS with animations
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

    .main {
        font-family: 'Roboto', sans-serif;
        padding: 2rem;
        animation: fadeIn 0.5s ease-in;
    }

    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    @keyframes slideIn {
        from { transform: translateY(20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }

    .stTextArea > div > div > textarea {
        background-color: #f8f9fa;
        border-radius: 10px;
        border: 2px solid #e9ecef;
        padding: 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }

    .stTextArea > div > div > textarea:focus {
        border-color: #80bdff;
        box-shadow: 0 0 0 0.2rem rgba(0,123,255,.25);
    }

    .result-card {
        padding: 20px;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        animation: slideIn 0.5s ease-out;
    }

    .explanation-item {
        padding: 0.5rem 1rem;
        margin: 0.5rem 0;
        border-radius: 5px;
        background-color: #f8f9fa;
        animation: fadeIn 0.5s ease-in;
    }

    .stButton>button {
        background-color: #007bff;
        color: white;
        border-radius: 10px;
        padding: 0.5rem 2rem;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        background-color: #0056b3;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    h1, h2, h3 {
        font-family: 'Roboto', sans-serif;
        font-weight: 500;
        color: #1a1a1a;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("✉️ Email Classification System")
    st.markdown("""
    <div style='animation: fadeIn 0.5s ease-in'>
        <p style='font-size: 1.2rem; color: #666; margin-bottom: 2rem;'>
            Analyze your emails for potential spam or harmful content
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Email input
    email_text = st.text_area(
        "Enter email content for classification:",
        height=200,
        placeholder="Paste your email content here..."
    )

    if st.button("Classify Email", type="primary"):
        if not email_text:
            st.error("Please enter some email content to classify.")
            return

        with st.spinner("🔍 Analyzing email content..."):
            # Process and classify email
            processed_text = st.session_state.text_processor.preprocess_text(email_text)
            features = st.session_state.text_processor.extract_features(email_text)
            classification, confidence, reasons = st.session_state.classifier.classify_email(features)

            # Display results with animation
            st.markdown(f"""
            <div class="result-card" style="
                background-color: {get_status_color(classification)};
                color: white;
                text-align: center;
            ">
                <h2 style="margin: 0; font-size: 2rem;">{classification}</h2>
                <p style="margin: 10px 0 0 0; font-size: 1.2rem;">Confidence: {confidence:.2%}</p>
            </div>
            """, unsafe_allow_html=True)

            # Analysis explanation
            st.markdown("### 📋 Analysis Explanation")
            for reason in reasons:
                st.markdown(f"""
                <div class="explanation-item">
                    ▪️ {reason}
                </div>
                """, unsafe_allow_html=True)

            # Display feature analysis in an expandable section
            with st.expander("🔍 View Detailed Analysis"):
                st.json(features)

if __name__ == "__main__":
    main()