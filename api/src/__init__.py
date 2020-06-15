from ..src.wrappers.MarianModelWrapper import MarianModelWrapper
from ..src.wrappers.GPT2ModelWrapper import GPT2ModelWrapper
from ..src.utils.utils import get_supported_languages, get_pretrained_weights
from transformers import MarianMTModel, MarianTokenizer
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from flask import Flask
from flask_cors import CORS

app = Flask(__name__, static_folder='../frontend/build')
CORS(app)

next_token_model_wrapper = GPT2ModelWrapper(GPT2LMHeadModel, GPT2Tokenizer, 'gpt2')

supported_languages = get_supported_languages()
pretrained_weights_for_supported_langs = get_pretrained_weights(supported_languages)

translation_model_wrappers = [MarianModelWrapper(MarianMTModel, MarianTokenizer,
                                                 pretrained_weights,
                                                 pretrained_weights_for_supported_langs[pretrained_weights])
                              for pretrained_weights in pretrained_weights_for_supported_langs.keys()]

messages = []

cookies = []
