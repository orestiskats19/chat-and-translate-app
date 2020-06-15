from api.src import supported_languages, messages, cookies, translation_model_wrappers, next_token_model_wrapper
from api.src import app
from flask import request

MESSAGES_THRESHOLD = 50


def store_message(message):
    if len(messages) > MESSAGES_THRESHOLD:
        messages.pop(0)
    messages.append(message)


def translation_is_supported(incoming_translation):
    return incoming_translation in supported_languages.keys()


def get_model_wrapper(incoming_translation):
    for model_wrapper in translation_model_wrappers:
        if incoming_translation in model_wrapper.supported_translations:
            return model_wrapper


@app.route('/translate', methods=['POST'])
def post_answer():
    json = request.json
    message = {"option": json["option"], "direction": json["direction"], "text": json["text"]}
    if translation_is_supported(message["option"]):
        model_wrapper = get_model_wrapper(message["option"])
        target_language = supported_languages[message["option"]]["target_language"]
        text = [f'>>{target_language}<< {message["text"]}']
        message["translation"] = model_wrapper.translator(text)
        store_message(message)
        return message["translation"]
    message["translation"] = "oops, we couldn't translate this"
    store_message(message)
    return {"translation": message["translation"]}


@app.route('/getMessages', methods=['GET'])
def get_messages():
    return {"messages": messages}
