
import streamlit as st
def load_styles():
    """Apply custom styling to the Streamlit application."""

    st.markdown("""
    <style>
    .stApp {
        background-color: #f6f8fc;
        color: #172033;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .hero {
        padding: 25px;
        border-radius: 16px;
        background: linear-gradient(
            120deg, #14213d, #1d5673
        );
        color: #ffffff;
        margin-bottom: 20px;
    }

    .hero h1 {
        color: #ffffff !important;
    }

    .hero p {
        color: #d9edf5 !important;
        font-size: 17px;
    }

    div[data-testid="stMetric"] {
        background: #ffffff;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #e5eaf1;
    }

    div[data-testid="stMetricLabel"] {
        color: #475569;
    }

    div[data-testid="stMetricValue"] {
        color: #14213d;
    }

    .stTextArea textarea {
        background-color: #ffffff;
        color: #172033;
    }

    </style>
    """, unsafe_allow_html=True)
