# code_explainer.py
import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from pygments.lexers import guess_lexer
from pygments.util import ClassNotFound

@st.cache_resource
def load_codet5():
    tokenizer = AutoTokenizer.from_pretrained("Salesforce/codet5-base")
    model = AutoModelForSeq2SeqLM.from_pretrained("Salesforce/codet5-base")
    return pipeline("text2text-generation", model=model, tokenizer=tokenizer)

codet5_pipe = load_codet5()

def explain_code_codet5(code):
    input_text = f"Summarize this function: {code}"
    result = codet5_pipe(input_text, max_length=100, do_sample=False)
    return result[0]["generated_text"]

def explain_code_deepseek(code):
    return "⚠️ DeepSeek model is disabled in local mode to avoid downloading large files."

def detect_language(code):
    try:
        lexer = guess_lexer(code)
        return lexer.name
    except ClassNotFound:
        return "Unknown"
