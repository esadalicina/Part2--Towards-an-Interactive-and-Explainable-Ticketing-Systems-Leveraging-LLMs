from keybert import KeyBERT
from transformers import pipeline

# Load a pre-trained transformer model using Hugging Face's pipeline
model_name = "sentence-transformers/all-MiniLM-L6-v2"
hf_pipeline = pipeline("feature-extraction", model=model_name)

# Initialize KeyBERT with the transformer model
kw_model = KeyBERT(model=hf_pipeline)


def tags(text):

        # Extract keywords
        keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 1), stop_words='english', top_n=3)

        # Extract just the keywords
        top_tags = [keyword[0] for keyword in keywords]
        return top_tags




