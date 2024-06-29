from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

# Load the pre-trained NER model and tokenizer
model_name = "dbmdz/bert-large-cased-finetuned-conll03-english"
model = AutoModelForTokenClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Create a NER pipeline
ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")


def extract_tags(text):
    # Use the NER pipeline to identify entities in the text
    entities = ner_pipeline(text)
    tags = [entity['word'].lower() for entity in entities]  # type: ignore # Convert tags to lowercase
    return tags


def tags(text):

    # Set to store unique tags
    unique_tags = set()

    # Extract tags from the ticket text
    tags = extract_tags(text)
    unique_tags.update(tags)  # Add the tags to the set of unique tags

    # Convert the set of unique tags back to a list
    return list(unique_tags)
