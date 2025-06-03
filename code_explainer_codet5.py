from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

tokenizer = AutoTokenizer.from_pretrained("Salesforce/codet5-base")
model = AutoModelForSeq2SeqLM.from_pretrained("Salesforce/codet5-base")

explain_pipe = pipeline("text2text-generation", model=model, tokenizer=tokenizer)

def explain_code(code):
    input_text = f"Summarize this function: {code}"
    result = explain_pipe(input_text, max_length=100, do_sample=False)
    return result[0]["generated_text"]
