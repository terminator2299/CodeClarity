import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

@st.cache_resource  # ✅ Cache model & tokenizer
def load_model():
    tokenizer = AutoTokenizer.from_pretrained("Salesforce/codet5-base")
    model = AutoModelForSeq2SeqLM.from_pretrained("Salesforce/codet5-base")
    return pipeline("text2text-generation", model=model, tokenizer=tokenizer)

explain_pipe = load_model()

def explain_code(code):
    input_text = f"Summarize this function: {code}"
    result = explain_pipe(input_text, max_length=100, do_sample=False)
    return result[0]["generated_text"]
