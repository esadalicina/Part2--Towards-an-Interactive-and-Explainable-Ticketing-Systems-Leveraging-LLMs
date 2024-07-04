from transformers import AutoTokenizer, T5ForConditionalGeneration
import streamlit as st

@st.cache
def load_model():
    tokenizer = AutoTokenizer.from_pretrained("czearing/article-title-generator")
    model = T5ForConditionalGeneration.from_pretrained("czearing/article-title-generator")
    return tokenizer, model

tokenizer, model = load_model()

def generate_title(text):
    input_ids = tokenizer(text, return_tensors="pt").input_ids
    outputs = model.generate(input_ids, max_new_tokens=500)
    title = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return title




