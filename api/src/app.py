from flask import Flask, request
from api.src import supported_languages, messages, cookies, model_wrappers
from flask_cors import CORS
import random


app = Flask(__name__, static_folder='../frontend/build')
CORS(app)

MESSAGES_THRESHOLD = 50


def store_message(message):
    if len(messages) > MESSAGES_THRESHOLD:
        messages.pop(0)
    messages.append(message)


def translation_is_supported(incoming_translation):
    return incoming_translation in supported_languages.keys()


def get_model_wrapper(incoming_translation):
    for model_wrapper in model_wrappers:
        if incoming_translation in model_wrapper.supported_translations:
            return model_wrapper.model, model_wrapper.tokenizer,


@app.route('/result', methods=['POST'])
def post_answer():
    json = request.json
    message = {"option": json["option"], "direction": json["direction"], "text": json["text"]}
    if translation_is_supported(message["option"]):
        trained_model, tokenizer = get_model_wrapper(message["option"])
        target_language = supported_languages[message["option"]]["target_language"]
        text = [f'>>{target_language}<< {message["text"]}']
        print(text)
        translated = trained_model.generate(**tokenizer.prepare_translation_batch(text))
        print(translated)
        print([tokenizer.decode(t, skip_special_tokens=True) for t in translated])
        message["translation"] = [tokenizer.decode(t, skip_special_tokens=True) for t in translated][0]
        store_message(message)
        return message["translation"]
    message["translation"] = "oops, we couldn't translate this"
    store_message(message)
    return message["translation"]


@app.route('/getMessages', methods=['GET'])
def get_messages():
    return {"messages": messages}


@app.route('/postCookie', methods=['POST'])
def post_cookie():
    n = random.choice(["1", "2", "3"])
    cookies.append(n)
    return {"cookie": n}


@app.route('/getCookies', methods=['GET'])
def get_stored_cookies():
    return {"cookies": str(cookies)}


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8020)
