import os
import json


def get_supported_languages():
    path_to_json = f'{os.getcwd()}/'

    for file_name in [file for file in os.listdir(path_to_json) if file.endswith('.json')]:
        with open(path_to_json + file_name) as json_file:
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
