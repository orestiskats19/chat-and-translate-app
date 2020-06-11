from ..src.wrappers.MarianModelWrapper import MarianModelWrapper
from ..src.utils.utils import get_supported_languages,get_models


supported_languages = get_supported_languages()
models = get_models(supported_languages)

model_wrappers = [MarianModelWrapper(model, models[model]) for model in models.keys()]

messages = []

cookies = []
