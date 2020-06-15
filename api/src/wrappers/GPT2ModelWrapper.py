import torch
from api.src.wrappers.ModelWrapper import ModelWrapper


class GPT2ModelWrapper(ModelWrapper):

    def __init__(self, model, tokenizer, pretrained_weights):
        super().__init__(model, tokenizer, pretrained_weights)

    def next_word_predictor(self, text):
        generated = self.tokenizer.encode(text)
        encoded_text = torch.tensor([generated])
        output, _ = self.model(encoded_text)
        _, token_indices = torch.topk(output[..., -1, :], k=5)
        return [self.tokenizer.decode([t]) for t in token_indices[0]]
