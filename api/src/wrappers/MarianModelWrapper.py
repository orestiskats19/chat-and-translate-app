from transformers import MarianMTModel, MarianTokenizer


class MarianModelWrapper:

    def __init__(self, model_name, supported_translations):
        self.model_name = model_name
        self.supported_translations = supported_translations
        self.tokenizer = self.__load_tokenizer()
        self.model = self.__load_model()

    def __load_tokenizer(self):
        return MarianTokenizer.from_pretrained(self.model_name)

    def __load_model(self):
        return MarianMTModel.from_pretrained(self.model_name)

