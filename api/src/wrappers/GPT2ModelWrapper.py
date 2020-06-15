from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch


class GPT2ModelWrapper:

    def __init__(self, model_name):
        self.model_name = model_name
        self.tokenizer = self.__load_tokenizer()
        self.model = self.__load_model()

    def __load_tokenizer(self):
        return GPT2Tokenizer.from_pretrained(self.model_name)

    def __load_model(self):
        return GPT2LMHeadModel.from_pretrained(self.model_name)

    def next_word_predictor(self, text):
        generated = self.tokenizer.encode(text)
        encoded_text = torch.tensor([generated])
        output = self.model(encoded_text)
        _, token_indices = torch.topk(output[..., -1, :], k=5)
        return [self.tokenizer.decode([t]) for t in token_indices[0]]
