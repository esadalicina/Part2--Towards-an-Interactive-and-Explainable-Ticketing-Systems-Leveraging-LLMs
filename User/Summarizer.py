from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize(text):
    summary = summarizer(text, max_length=35, min_length=5, do_sample=True)
    return summary

