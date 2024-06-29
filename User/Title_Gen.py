from transformers import AutoTokenizer, T5ForConditionalGeneration


tokenizer = AutoTokenizer.from_pretrained("czearing/article-title-generator")
model = T5ForConditionalGeneration.from_pretrained("czearing/article-title-generator")


def generate_title(text):
    input_ids = tokenizer(text, return_tensors="pt").input_ids
    outputs = model.generate(input_ids, max_new_tokens=500)
    title = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return title




