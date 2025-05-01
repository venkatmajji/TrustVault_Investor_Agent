

from langchain_community.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain

from langchain_community.embeddings import OpenAIEmbeddings


from langchain.vectorstores import FAISS
from langchain.document_loaders import PyPDFLoader, TextLoader
import streamlit as st
import datetime

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

llm = ChatOpenAI(model_name="gpt-4o", temperature=0)
qa = ConversationalRetrievalChain.from_llm(llm, vectorstore.as_retriever())

def log_to_trustvault(question, answer):
    timestamp = datetime.datetime.now().isoformat()
    with open("trustvault_log.txt", "a") as f:
        f.write(f"[{timestamp}] Q: {question}\nA: {answer}\n\n")

st.set_page_config(page_title="TrustVault Investor Pitch Agent", layout="centered")

st.markdown("""
<style>
.chat-box {background-color: #f9fafb; padding: 20px; border-radius: 12px; border: 1px solid #e5e7eb; margin-bottom: 20px;}
.button-primary {background-color: #2563eb; color: white; padding: 10px 20px; border-radius: 8px; text-decoration: none; display: inline-block;}
</style>
""", unsafe_allow_html=True)

st.title("🚀 TrustVault Investor Agent")
st.subheader("Your interactive AI pitch companion.")
st.write("Ask anything about our vision, roadmap, traction, market opportunity, and why now.")

with st.expander("View example questions"):
    st.write("- What problem does TrustVault solve?")
    st.write("- How big is the market?")
    st.write("- How do you make money?")
    st.write("- Why now?")
    st.write("- Who is on your team?")

chat_history = []

query = st.text_input("Ask your question here:")
if query:
    result = qa({'question': query, 'chat_history': chat_history})
    answer = result['answer']
    st.markdown(f"<div class='chat-box'><b>You:</b> {query}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='chat-box'><b>TrustVault Agent:</b> {answer}</div>", unsafe_allow_html=True)
    chat_history.append((query, answer))
    log_to_trustvault(query, answer)

st.markdown("<hr><p style='text-align:center; color: gray;'>© 2025 TrustVault.ai — All rights reserved.</p>", unsafe_allow_html=True)
