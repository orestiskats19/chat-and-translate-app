import os
import json


def get_supported_languages():
    with open("../../supported_languages.json") as json_file:
        data = json.load(json_file)
        return data


def get_pretrained_weights(supported_languages):
    model = {}
    for lang in supported_languages.keys():
        if supported_languages[lang]["model"] in model.keys():
            model[supported_languages[lang]["model"]].append(lang)
        else:
            model[supported_languages[lang]["model"]] = [lang]
    return model
