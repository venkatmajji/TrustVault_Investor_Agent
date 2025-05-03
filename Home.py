
import streamlit as st

st.set_page_config(page_title="TrustVault - Immutable Audit Layer for AI", page_icon="🔒", layout="wide")

st.markdown("""
<style>
.header-title {font-size: 50px;color: #2563eb;font-weight: bold;text-align: center;margin-bottom: 20px;margin-top: 30px;}
.subheader-text {text-align: center;color: #4b5563;margin-bottom: 40px;font-size: 22px;}
.section-header {background-color: #eff6ff;padding: 14px;border-radius: 8px;color: #2563eb;font-weight: bold;text-align: center;font-size: 26px;margin-bottom: 10px;}
.link-box {background-color: #ffffff;padding: 24px;border-radius: 12px;border: 2px solid #2563eb;margin: 10px;text-align: center;}
.link-box a {text-decoration: none; color: #2563eb; font-size: 20px; font-weight: bold;}
.link-box:hover {background-color: #dbeafe;}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='header-title'>TrustVault</div>", unsafe_allow_html=True)
st.markdown("<div class='subheader-text'>The Immutable Audit Layer for AI & LLMs — Capture, Certify, Verify.</div>", unsafe_allow_html=True)
st.markdown("<div class='section-header'>🚀 Explore TrustVault</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class='link-box'>
        <a href="/Investor_Pitch_Agent">💼 Investor Agent → Learn and Ask About Our Company</a>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='link-box'>
        <a href="mailto:founder@trustvault.ai">📩 Contact Founders → Book Intro Call</a>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<hr>
<p style='text-align:center; color: gray;'>© 2025 TrustVault.ai — All rights reserved.</p>
""", unsafe_allow_html=True)
