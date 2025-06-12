# app.py
import streamlit as st
st.set_page_config(page_title="CodeClarity", layout="centered")  # 👈 This must come immediately after imports

from code_explainer import explain_code_codet5, explain_code_deepseek, detect_language

st.title("🧠 CodeClarity: Explain Code with AI")

uploaded_file = st.file_uploader("Upload your code file (.py, .js, .java, etc.)", type=["py", "js", "java", "cpp", "ts", "go", "php", "rb"])

code_input = ""

if uploaded_file is not None:
    code_bytes = uploaded_file.read()
    code_input = code_bytes.decode("utf-8")
    st.code(code_input, language="auto")
else:
    code_input = st.text_area("Or paste your code here:", height=200)

if code_input.strip():
    detected_lang = detect_language(code_input)
    st.markdown(f"🔍 **Detected Language:** `{detected_lang}`")

    model_choice = "CodeT5 (Fast)"  # Only CodeT5 for now
    mode = st.radio("Choose explanation mode:", ["Full function", "Line-by-line"])

    if st.button("Explain"):
        with st.spinner("Generating explanation..."):
            if mode == "Full function":
                output = explain_code_codet5(code_input)
                st.success("Explanation:")
                st.write(output)
            else:
                lines = code_input.strip().split('\n')
                st.success("Line-by-line Explanation:")
                for i, line in enumerate(lines):
                    if line.strip():
                        with st.expander(f"Line {i+1}: `{line.strip()}`"):
                            explanation = explain_code_codet5(line)
                            st.write(explanation)
else:
    st.warning("Please upload or paste some code first.")
