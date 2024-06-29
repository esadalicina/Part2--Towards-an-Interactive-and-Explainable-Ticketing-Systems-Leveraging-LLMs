from transformers import MBartForConditionalGeneration, MBart50TokenizerFast


model_name = "facebook/mbart-large-50-many-to-many-mmt"

# Load the MBart model and tokenizer
model = MBartForConditionalGeneration.from_pretrained(model_name)
tokenizer = MBart50TokenizerFast.from_pretrained(model_name)

text = "I am a student."

def translate_text(text, src_lang, tgt_lang):
    tokenizer.src_lang = src_lang
    encoded_text = tokenizer(text, return_tensors="pt")
    generated_tokens = model.generate(
        **encoded_text,
        forced_bos_token_id=tokenizer.lang_code_to_id[tgt_lang]
    )
    return tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]


def german(text):
    translated_to_german = translate_text(text, 'en_XX', 'de_DE')
    return translated_to_german


def french(text):
    translated_to_french = translate_text(text, 'en_XX', 'fr_XX')
    return translated_to_french


german(text)
french(text)
