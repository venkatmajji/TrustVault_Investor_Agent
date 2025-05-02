# Investor Pitch Agent - Production Ready Landing Page with Smart Suggestions + Session Memory + Downloadable Slides + Auto Email

from langchain_community.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import PyPDFLoader
import streamlit as st
import random
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# --- Email sending utility ---
def send_pitch_deck_email(receiver_email):
    sender_email = st.secrets["EMAIL_ADDRESS"]
    sender_password = st.secrets["EMAIL_PASSWORD"]

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "TrustVault Pitch Deck + Thank You"

    body = "Thank you for your interest in TrustVault! Please find attached our latest investor pitch deck. Feel free to reply to this email or book a time with our founder for deeper discussion."
    msg.attach(MIMEBase('application', 'octet-stream'))

    # Attach PDF
    filename = "TrustVault_Pitch_Deck.pdf"
    with open("TrustVault_Investor_One_Pager.pdf", "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )
    msg.attach(part)

    # Send email
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

# --- Load documents (PDF + One Pager + Landing Page Summary) ---
pdf_loader = PyPDFLoader("TrustVault_Investor_One_Pager.pdf")
pdf_docs = pdf_loader.load()
pdf_texts = [d.page_content for d in pdf_docs]

additional_docs = [
    "TrustVault is the immutable audit layer for AI and LLMs. Capture, certify, and verify all interactions.",
    "Product: SDK + WORM storage + Merkle hashing + daily PDF seals + Evaluator Marketplace.",
    "TAM: $15B+, SAM: $2.5B, SOM: $100M wedge from regulated AI teams.",
    "Business model: Free → $199 Pro → $999 Compliance → $50k+ Enterprise.",
    "Roadmap: Immutable Vault → Real-time evaluator proxy → Evaluator Marketplace → Compliance automation.",
    "Why now: EU AI Act, SOC 2, HIPAA and enterprise AI buyers all need traceability today.",
    "Competitive edge: Only product with WORM+Merkle+root cert + marketplace + audit-first design."
]

all_docs = pdf_texts + additional_docs

# --- Embed and index ---
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = FAISS.from_texts(all_docs, embeddings)

# --- Create memory (session based) ---
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# --- Create conversational retrieval chain with memory ---
llm = ChatOpenAI(model_name="gpt-4-1106-preview", temperature=0)
qa = ConversationalRetrievalChain.from_llm(llm, vectorstore.as_retriever(), memory=memory)

# --- TrustVault logger prototype ---
def log_to_trustvault(question, answer):
    timestamp = datetime.datetime.now().isoformat()
    with open("trustvault_log.txt", "a") as f:
        f.write(f"[{timestamp}] Q: {question}\nA: {answer}\n\n")

# --- Streamlit UI (Production Landing Page) ---
st.set_page_config(page_title="TrustVault Investor Pitch Agent", page_icon="📊", layout="wide")

st.markdown("""
<style>
.chat-box {background-color: #f9fafb;padding: 20px;border-radius: 12px;border: 1px solid #e5e7eb;margin-bottom: 20px;}
.header-title {font-size: 42px;color: #2563eb;font-weight: bold;text-align: center;margin-bottom: 10px;margin-top: 10px;}
.subheader-text {text-align: center;color: gray;margin-bottom: 20px;font-size: 18px;}
.cta-button {background-color: #2563eb;color: white;padding: 12px 24px;border-radius: 8px;text-decoration: none;font-weight: bold;display: inline-block;}
.section-header {background-color: #eff6ff;padding: 10px;border-radius: 8px;color: #2563eb;font-weight: bold;text-align: center;font-size: 20px;margin-bottom: 10px;}
</style>
""", unsafe_allow_html=True)

st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Flat_tick_icon.svg/2048px-Flat_tick_icon.svg.png", width=80)
st.markdown("<div class='header-title'>TrustVault Investor Agent</div>", unsafe_allow_html=True)
st.markdown("<div class='subheader-text'>Ask our AI agent or browse/download the pitch deck below. Your questions answered in real-time.</div>", unsafe_allow_html=True)

st.markdown("<div class='section-header'>💬 Ask TrustVault Investor Agent</div>", unsafe_allow_html=True)

example_questions = [
    "What problem does TrustVault solve?",
    "How do you make money?",
    "What is your roadmap for the next 12 months?",
    "Who is your competition?",
    "How big is the market opportunity?",
    "Why should we invest?"
]

cols = st.columns(2)
for idx, q in enumerate(example_questions):
    col = cols[idx % 2]
    with col:
        if st.button(f"👉 {q}", key=q):
            clicked_question = q

clicked_question = None

query = clicked_question or st.text_input("Ask your question here:")

if query:
    result = qa({'question': query})
    answer = result['answer']
    st.markdown(f"<div class='chat-box'><b>You:</b> {query}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='chat-box'><b>TrustVault Agent:</b> {answer}</div>", unsafe_allow_html=True)
    log_to_trustvault(query, answer)

    st.markdown("#### Suggested Next Question:")
    suggested_question = random.choice([q for q in example_questions if q != query])
    if st.button(f"➡️ {suggested_question}"):
        query = suggested_question

st.markdown("<div class='section-header'>📊 Investor Pitch Deck Viewer & Download</div>", unsafe_allow_html=True)
#st.components.v1.iframe("https://docs.google.com/presentation/d/e/2PACX-1vQDzXXXXX-YOUR-SLIDES-URL-HERE/embed?start=false&loop=false&delayms=3000", height=550)
st.components.v1.iframe("https://docs.google.com/presentation/d/e/2PACX-1vSDzdc5x-xYZn3vCGhBiUxtK0Tmdkd9ufjXmja6mMaLcIyLkR9M61j_YszleNivSA/embed?start=false&loop=false&delayms=3000", height=550)


st.markdown("### 📥 Download Pitch Deck PDF")
with st.form("download_form"):
    email = st.text_input("Enter your email to download the pitch deck")
    submitted = st.form_submit_button("Send me the deck")

    if submitted and email:
        st.success(f"Thank you! We'll email you the deck shortly at {email}.")
        send_pitch_deck_email(email)
        with open("investor_emails.txt", "a") as log:
            log.write(f"{datetime.datetime.now().isoformat()} - {email}\n")

st.markdown("""
<hr>
<p style='text-align:center; color: gray;'>Interested in learning more or booking an intro call?</p>
<p style='text-align:center;'><a class='cta-button' href='mailto:founder@trustvault.ai'>📩 Book Investor Intro Call</a></p>
<p style='text-align:center; color: gray;'>© 2025 TrustVault.ai — All rights reserved.</p>
""", unsafe_allow_html=True)
