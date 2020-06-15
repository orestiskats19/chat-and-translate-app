from flask import Flask, request
from api.src import supported_languages, messages, cookies, translation_model_wrappers, next_token_model_wrapper
from flask_cors import CORS
import uuid

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
    for model_wrapper in translation_model_wrappers:
        if incoming_translation in model_wrapper.supported_translations:
            return model_wrapper


@app.route('/result', methods=['POST'])
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


@app.route('/next_word_predictor', methods=['POST'])
def post_next_word():
    input_json = request.json
    if input_json["text"] and not input_json["text"].startswith(" "):
        tokens = next_token_model_wrapper.next_word_predictor(input_json["text"])
        return {"tokens": tokens}
    return {"tokens": []}


@app.route('/getMessages', methods=['GET'])
def get_messages():
    return {"messages": messages}


@app.route('/postCookies', methods=['POST'])
def get_stored_cookies():
    input_json = request.json
    if "cookie" in input_json.keys() and cookies:
        if any([input_json["cookie"] in str(cook.values()) for cook in cookies]):
            return {
                "cookies": {"role": [str(cook["role"]) if input_json["cookie"] in str(cook.values())
                                     else None
                                     for cook in cookies][0],
                            "cookie": input_json["cookie"]}}
    cookie = {}
    if len(cookies) == 0:
        cookie["role"] = "master"
        cookie["cookie"] = uuid.uuid4()
        cookies.append(cookie)
        return {"cookies": cookie}
    elif len(cookies) == 1:
        cookie["role"] = "friend"
        cookie["cookie"] = uuid.uuid4()
        cookies.append(cookie)
        return {"cookies": cookie}

    return {"cookies": cookie}



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8020)
