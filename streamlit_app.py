import streamlit as st
import toml
import os
from utils.crawler import crawl
from utils.content_extractor import extract_clean_text
from utils.module_agent import extract_modules

st.set_page_config(page_title="Pulse – Module Extraction AI Agent", layout="wide")

st.title("📦 Pulse – Module Extraction AI Agent")
st.write("AI-powered application to extract modules and submodules from documentation-based help websites.")

config = toml.load("config.toml")
os.makedirs(config["output"]["output_dir"], exist_ok=True)

urls_input = st.text_area("Enter documentation URLs (one per line)")
api_key_input = st.text_input("OpenAI API Key", type="password", help="Enter key or set OPENAI_API_KEY env var.")

if st.button("🚀 Extract Modules"):
    urls = [u.strip() for u in urls_input.split("\n") if u.strip()]
    combined_text = ""
    for url in urls:
        pages = crawl(url, config["app"]["max_depth"], config["crawler"]["max_pages"])
        for _, soup in pages:
            combined_text += extract_clean_text(soup) + "\n"
    api_key = api_key_input or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        st.error("Missing OpenAI API Key. Provide it above or set OPENAI_API_KEY.")
    else:
        try:
            result = extract_modules(combined_text, config["llm"]["model"], api_key)
            st.json(result)
        except Exception as e:
            st.error(f"Extraction failed: {e}")
