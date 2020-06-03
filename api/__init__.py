from transformers import MarianMTModel, MarianTokenizer

model_name_english = 'Helsinki-NLP/opus-mt-en-ROMANCE'
tokenizer_english = MarianTokenizer.from_pretrained(model_name_english)
model_english = MarianMTModel.from_pretrained(model_name_english)

model_name_spanish = 'Helsinki-NLP/opus-mt-aed-es'
tokenizer_spanish = MarianTokenizer.from_pretrained(model_name_spanish)
model_spanish = MarianMTModel.from_pretrained(model_name_spanish)
