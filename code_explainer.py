# code_explainer.py
import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForCausalLM, pipeline
from pygments.lexers import guess_lexer
from pygments.util import ClassNotFound
import torch

@st.cache_resource
def load_codet5():
    tokenizer = AutoTokenizer.from_pretrained("Salesforce/codet5-base")
    model = AutoModelForSeq2SeqLM.from_pretrained("Salesforce/codet5-base")
    return pipeline("text2text-generation", model=model, tokenizer=tokenizer)

@st.cache_resource
def load_deepseek():
    tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/deepseek-coder-6.7b-instruct", trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        "deepseek-ai/deepseek-coder-6.7b-instruct",
        trust_remote_code=True,
        torch_dtype=torch.float16,
        device_map="auto"
    )
    return pipeline("text-generation", model=model, tokenizer=tokenizer, device=0, max_new_tokens=200)

codet5_pipe = load_codet5()
deepseek_pipe = load_deepseek()

def explain_code_codet5(code):
    input_text = f"Summarize this function: {code}"
    result = codet5_pipe(input_text, max_length=100, do_sample=False)
    return result[0]["generated_text"]

def explain_code_deepseek(code):
    prompt = f"Explain what the following code does:\n{code}\n"
    result = deepseek_pipe(prompt)
    return result[0]["generated_text"].strip()



def detect_language(code):
    try:
        lexer = guess_lexer(code)
        return lexer.name
    except ClassNotFound:
        return "Unknown"

