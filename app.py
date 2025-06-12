# app.py
import streamlit as st
from code_explainer import explain_code_codet5, explain_code_deepseek, detect_language

st.set_page_config(page_title="CodeClarity", layout="centered")
st.title("🧠 CodeClarity: Explain Code with AI")

st.markdown("""
Upload your source code or paste it below, and let AI explain it for you!
Choose from two powerful models: **CodeT5 (Fast)** and **DeepSeek (More Accurate)**.
""")

# File uploader
uploaded_file = st.file_uploader(
    "📄 Upload your code file (.py, .js, .java, etc.):",
    type=["py", "js", "java", "cpp", "ts", "go", "php", "rb"]
)

code_input = ""

if uploaded_file is not None:
    code_input = uploaded_file.read().decode("utf-8")
    st.code(code_input, language="auto")
else:
    code_input = st.text_area("✍️ Or paste your code here:", height=200)

# Process code
if code_input.strip():
    # Language detection
    detected_lang = detect_language(code_input)
    st.markdown(f"🧠 **Detected Language:** `{detected_lang}`")

    # Model and mode selectors
    model_choice = st.selectbox("🤖 Select AI model:", ["CodeT5 (Fast)", "DeepSeek Coder (More Powerful)"])
    mode = st.radio("🧩 Choose explanation mode:", ["Full function", "Line-by-line"])

    if st.button("🚀 Explain Code"):
        with st.spinner("Analyzing and explaining your code..."):
            if mode == "Full function":
                output = (
                    explain_code_codet5(code_input)
                    if model_choice == "CodeT5 (Fast)"
                    else explain_code_deepseek(code_input)
                )
                st.success("📘 Full Explanation:")
                st.markdown(output)
            else:
                lines = code_input.strip().split('\n')
                st.success("🔍 Line-by-Line Explanation:")
                for i, line in enumerate(lines):
                    if line.strip():
                        with st.expander(f"Line {i+1}: `{line.strip()}`"):
                            explanation = (
                                explain_code_codet5(line)
                                if model_choice == "CodeT5 (Fast)"
                                else explain_code_deepseek(line)
                            )
                            st.markdown(explanation)
else:
    st.info("👆 Upload or paste your code above to get started.")
