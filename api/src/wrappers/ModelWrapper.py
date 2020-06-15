
class ModelWrapper:

    def __init__(self, model, tokenizer, pretrained_weights):
        self.tokenizer = tokenizer.from_pretrained(pretrained_weights)
        self.model = model.from_pretrained(pretrained_weights)
