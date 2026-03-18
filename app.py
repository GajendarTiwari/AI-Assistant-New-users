import streamlit as st
import requests

# API Keys
GEMINI_API_KEY = ""
NEWS_API_KEY = ""

# Gemini API function
def ask_gemini(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    if "candidates" in result:
        return result["candidates"][0]["content"]["parts"][0]["text"]
    elif "error" in result:
        code = result["error"]["code"]
        if code == 429:
            return "⚠️ Too many requests — please wait 1-2 minutes and try again!"
        return f"⚠️ API Error: {result['error']['message']}"
    return "⚠️ Something went wrong, please try again."

# Page config
st.set_page_config(
    page_title="AI Assistant | Cara",
    page_icon="🤖",
    layout="wide"
)

# Sidebar - AI News
with st.sidebar:
    st.title("📰 Today's AI News")
    st.caption("Latest AI tools & updates")
    if st.button("🔄 Refresh News"):
        st.rerun()
    try:
        news_url = f"https://newsapi.org/v2/everything?q=artificial+intelligence+tools&sortBy=publishedAt&pageSize=5&apiKey={NEWS_API_KEY}"
        news_response = requests.get(news_url)
        news = news_response.json()
        if news["status"] == "ok":
            for article in news["articles"]:
                st.markdown(f"**{article['title']}**")
                st.caption(article["source"]["name"])
                st.markdown(f"[Read more]({article['url']})")
                st.divider()
        else:
            st.info("Could not load news right now.")
    except:
        st.info("Could not load news right now.")

# Header
st.title("🤖 AI Assistant for Cara")
st.caption("Hi Cara! 👋 Your personal guide to understanding and building with AI")
st.markdown("---")

# Tabs
tab1, tab2, tab3 = st.tabs(["💡 Ask & Learn", "🛠️ POC Ideas", "🤖 Mini QA Bot"])

# Tab 1 - Ask & Learn
with tab1:
    st.subheader("Ask me anything about AI!")
    st.markdown("No technical background needed — ask in plain English.")
    question = st.text_input("Your question:", placeholder="e.g. What is AI? How can AI help my business?")
    if st.button("Ask", key="ask"):
        if question:
            with st.spinner("Thinking..."):
                prompt = f"""
                You are a friendly AI expert explaining concepts to a business professional
                with no technical background. Answer clearly, avoid jargon, and always give
                a real-world business example. Keep it concise and engaging.
                Question: {question}
                """
                answer = ask_gemini(prompt)
                st.success("Here's your answer:")
                st.write(answer)
        else:
            st.warning("Please type a question first!")

# Tab 2 - POC Ideas
with tab2:
    st.subheader("AI Use Case Ideas for Your Business")
    st.markdown("Tell me about your business and I'll suggest AI POCs you can build.")
    business_desc = st.text_area("Describe your business or department:",
                                  placeholder="e.g. We manage quality control for a manufacturing company...")
    if st.button("Generate Ideas", key="ideas"):
        if business_desc:
            with st.spinner("Generating ideas..."):
                prompt = f"""
                You are an AI consultant. Based on the business description below, suggest
                3-5 practical AI POC ideas. For each idea include:
                - What it does
                - Business benefit
                - How hard it is to build (Easy/Medium/Hard)
                Keep it simple and business-focused, no technical jargon.
                Business: {business_desc}
                """
                answer = ask_gemini(prompt)
                st.success("Here are your AI POC ideas:")
                st.write(answer)
        else:
            st.warning("Please describe your business first!")

# Tab 3 - Mini QA Bot
with tab3:
    st.subheader("Mini QA Bot Demo")
    st.markdown("Paste any text, then ask questions about it — this is exactly what a QA bot does!")
    document = st.text_area("Paste your document or text here:", height=200,
                             placeholder="Paste any company document, policy, or text...")
    user_question = st.text_input("Ask a question about the text:",
                                   placeholder="e.g. What is the main point?")
    if st.button("Get Answer", key="qa"):
        if document and user_question:
            with st.spinner("Reading document..."):
                prompt = f"""
                Based ONLY on the document below, answer the question clearly and concisely.
                If the answer is not in the document, say so honestly.
                Document: {document}
                Question: {user_question}
                """
                answer = ask_gemini(prompt)
                st.success("Answer:")
                st.write(answer)
        else:
            st.warning("Please paste a document and ask a question!")
