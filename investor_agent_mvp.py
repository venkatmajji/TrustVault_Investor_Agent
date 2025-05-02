# Investor Pitch Agent - Production Ready Landing Page

from langchain_community.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import PyPDFLoader
import streamlit as st
import datetime

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

# --- Create conversational retrieval chain ---
llm = ChatOpenAI(model_name="gpt-4o", temperature=0)
qa = ConversationalRetrievalChain.from_llm(llm, vectorstore.as_retriever())

# --- TrustVault logger prototype ---
def log_to_trustvault(question, answer):
    timestamp = datetime.datetime.now().isoformat()
    with open("trustvault_log.txt", "a") as f:
        f.write(f"[{timestamp}] Q: {question}\nA: {answer}\n\n")

# --- Streamlit UI (Production Landing Page) ---
st.set_page_config(page_title="TrustVault Investor Pitch Agent", page_icon="📊", layout="wide")

st.markdown("""
<style>
.chat-box {
    background-color: #f9fafb;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
    margin-bottom: 20px;
}
.header-title {
    font-size: 42px;
    color: #2563eb;
    font-weight: bold;
    text-align: center;
    margin-bottom: 10px;
    margin-top: 10px;
}
.subheader-text {
    text-align: center;
    color: gray;
    margin-bottom: 40px;
    font-size: 18px;
}
.cta-button {
    background-color: #2563eb;
    color: white;
    padding: 12px 24px;
    border-radius: 8px;
    text-decoration: none;
    font-weight: bold;
    display: inline-block;
}
</style>
""", unsafe_allow_html=True)

# Logo and Header
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Flat_tick_icon.svg/2048px-Flat_tick_icon.svg.png", width=80)
st.markdown("<div class='header-title'>TrustVault Investor Agent</div>", unsafe_allow_html=True)
st.markdown("<div class='subheader-text'>Your interactive pitch — explore our roadmap, deck, and ask anything live below.</div>", unsafe_allow_html=True)

# Layout with 2 columns
col1, col2 = st.columns([1, 1])

# Pitch deck embedded viewer
with col1:
    st.write("### 📊 Investor Pitch Deck Viewer")
    st.components.v1.iframe("https://docs.google.com/presentation/d/e/2PACX-1vSDzdc5x-xYZn3vCGhBiUxtK0Tmdkd9ufjXmja6mMaLcIyLkR9M61j_YszleNivSA/embed?start=false&loop=false&delayms=3000", height=550)



# Chat agent UI
with col2:
    st.write("### 💬 Ask TrustVault Investor Agent")

    chat_history = []

    query = st.text_input("Ask your question here:")
    if query:
        result = qa({'question': query, 'chat_history': chat_history})
        answer = result['answer']

        st.markdown(f"<div class='chat-box'><b>You:</b> {query}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='chat-box'><b>TrustVault Agent:</b> {answer}</div>", unsafe_allow_html=True)

        chat_history.append((query, answer))
        log_to_trustvault(query, answer)

st.markdown("""
<hr>
<p style='text-align:center; color: gray;'>Interested in learning more or booking an intro call?</p>
<p style='text-align:center;'><a class='cta-button' href='mailto:founder@trustvault.ai'>📩 Book Investor Intro Call</a></p>
<p style='text-align:center; color: gray;'>© 2025 TrustVault.ai — All rights reserved.</p>
""", unsafe_allow_html=True)
