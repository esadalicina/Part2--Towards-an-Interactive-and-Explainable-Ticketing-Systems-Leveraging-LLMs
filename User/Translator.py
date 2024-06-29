from transformers import MBartForConditionalGeneration, MBart50TokenizerFast


model_name = "facebook/mbart-large-50-many-to-many-mmt"

# Load the MBart model and tokenizer
model = MBartForConditionalGeneration.from_pretrained(model_name)
tokenizer = MBart50TokenizerFast.from_pretrained(model_name)

def translate_text(text, src_lang, tgt_lang):
    tokenizer.src_lang = src_lang
    encoded_text = tokenizer(text, return_tensors="pt")
    generated_tokens = model.generate(
        **encoded_text,
        forced_bos_token_id=tokenizer.lang_code_to_id[tgt_lang]
    )
    return tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]

# Example ticket text
ticket_text = "The server is down and needs to be restarted."

# Translate the ticket to German
translated_to_german = translate_text(ticket_text, 'en_XX', 'de_DE')
print("Translated to German:", translated_to_german)

# Translate the ticket to French
translated_to_french = translate_text(ticket_text, 'en_XX', 'fr_XX')
print("Translated to French:", translated_to_french)


# Save the model and tokenizer
model.save_pretrained("/home/users/elicina/Master-Thesis/Models/Translater")
tokenizer.save_pretrained("/home/users/elicina/Master-Thesis/Models/Tok-Translater")

print("Model and tokenizer saved successfully.")