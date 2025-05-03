import streamlit as st
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import PyPDFLoader
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def send_pitch_deck_email(receiver_email):
    sender_email = st.secrets["EMAIL_ADDRESS"]
    sender_password = st.secrets["EMAIL_PASSWORD"]
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = "TrustVault Pitch Deck + Thank You"

    filename = "TrustVault_Investor_One_Pager.pdf"
    with open(filename, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename= {filename}")
    msg.attach(part)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

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

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = FAISS.from_texts(all_docs, embeddings)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
llm = ChatOpenAI(model_name="gpt-4o", temperature=0)
qa = ConversationalRetrievalChain.from_llm(llm, vectorstore.as_retriever(), memory=memory)

st.set_page_config(page_title="TrustVault Investor Agent", page_icon="📊", layout="wide")

st.markdown("""
<style>
.chat-box {background-color: #f9fafb;padding: 20px;border-radius: 12px;border: 1px solid #e5e7eb;margin-bottom: 20px;}
.header-title {font-size: 42px;color: #2563eb;font-weight: bold;text-align: center;margin-bottom: 10px;margin-top: 10px;}
.subheader-text {text-align: center;color: #2563eb;margin-bottom: 20px;font-size: 18px;}
.cta-button {background-color: #2563eb;color: white;padding: 12px 24px;border-radius: 8px;text-decoration: none;font-weight: bold;display: inline-block;}
.section-header {background-color: #eff6ff;padding: 10px;border-radius: 8px;color: #2563eb;font-weight: bold;text-align: center;font-size: 20px;margin-bottom: 10px;}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='header-title'>TrustVault Investor Agent</div>", unsafe_allow_html=True)
st.markdown("<div class='subheader-text'><b>TrustVault solves the problem...</b></div>", unsafe_allow_html=True)
st.markdown("<div class='section-header'>💬 Ask TrustVault Investor Agent</div>", unsafe_allow_html=True)

if "user_query" not in st.session_state:
    st.session_state.user_query = ""
if "answer" not in st.session_state:
    st.session_state.answer = ""
if "selected_question" not in st.session_state:
    st.session_state.selected_question = ""

example_questions = [
    "👉 What problem does TrustVault solve?",
    "👉 How do you make money?",
    "👉 What is your roadmap for the next 12 months?",
    "👉 Who is your competition?",
    "👉 How big is the market opportunity?",
    "👉 Why should we invest?"
]

st.markdown("#### Example Questions (Click to Ask)")
cols = st.columns(3)
for idx, q in enumerate(example_questions):
    if cols[idx % 3].button(q, key=q):
        st.session_state.selected_question = q
        st.session_state.user_query = ""
        st.session_state.answer = ""

if st.session_state.selected_question:
    result = qa({'question': st.session_state.selected_question})
    st.session_state.answer = result['answer']
    st.markdown(f"<div class='chat-box'><b>TrustVault Agent:</b> {st.session_state.answer.replace('\n', '<br>')}</div>", unsafe_allow_html=True)

user_query = st.text_input("Or type your own question here:", value=st.session_state.user_query)
if user_query:
    st.session_state.user_query = user_query
    st.session_state.selected_question = ""
    result = qa({'question': user_query})
    st.session_state.answer = result['answer']
    st.markdown(f"<div class='chat-box'><b>TrustVault Agent:</b> {st.session_state.answer.replace('\n', '<br>')}</div>", unsafe_allow_html=True)

st.components.v1.iframe("https://docs.google.com/presentation/d/e/2PACX-1vSDzdc5x-xYZn3vCGhBiUxtK0Tmdkd9ufjXmja6mMaLcIyLkR9M61j_YszleNivSA/embed?start=false&loop=false&delayms=3000", height=550)

st.markdown("### 📥 Download Pitch Deck PDF")
with st.form("download_form"):
    email = st.text_input("Enter your email to download the pitch deck")
    submitted = st.form_submit_button("Send me the deck")
    if submitted and email:
        st.success(f"Thank you! We'll email you the deck shortly at {email}.")
        send_pitch_deck_email(email)
