from transformers import AutoTokenizer, T5ForConditionalGeneration


tokenizer = AutoTokenizer.from_pretrained("czearing/article-title-generator")
model = T5ForConditionalGeneration.from_pretrained("czearing/article-title-generator")

text = "I am having trouble logging into my bank account. I have tried multiple times and " \
       "I have received no response. I tried resetting my password, but that did not seem to work either." \
       "I am concerned that there may be an issue with my account security or that someone " \
       "has accessed my account without my permission."


def generate_title(text):
    input_ids = tokenizer(text, return_tensors="pt").input_ids
    outputs = model.generate(input_ids, max_new_tokens=500)
    title = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return title


print(generate_title(text))



