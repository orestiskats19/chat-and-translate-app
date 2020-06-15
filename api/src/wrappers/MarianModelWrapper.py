from api.src.wrappers.ModelWrapper import ModelWrapper


class MarianModelWrapper(ModelWrapper):

    def __init__(self, model, tokenizer, pretrained_weights, supported_translations):
        super().__init__(model, tokenizer, pretrained_weights)
        self.supported_translations = supported_translations

    def translator(self, text):
        encoded_translation = self.model.generate(**self.tokenizer.prepare_translation_batch(text))
        return [self.tokenizer.decode(t, skip_special_tokens=True) for t in encoded_translation][0]

