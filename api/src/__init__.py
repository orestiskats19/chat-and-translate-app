from ..src.wrappers.MarianModelWrapper import MarianModelWrapper
from ..src.wrappers.GPT2ModelWrapper import GPT2ModelWrapper
from ..src.utils.utils import get_supported_languages,get_models

next_token_model_wrapper = GPT2ModelWrapper('gpt2')

supported_languages = get_supported_languages()
models = get_models(supported_languages)

translation_model_wrappers = [MarianModelWrapper(model, models[model]) for model in models.keys()]

messages = []

cookies = []
