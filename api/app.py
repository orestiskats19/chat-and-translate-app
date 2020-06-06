from flask import Flask, request
from api import model_english, model_spanish, tokenizer_english, tokenizer_spanish, messages, cookies
from flask_cors import CORS
import random
app = Flask(__name__, static_folder='../frontend/build')
CORS(app)

MESSAGES_THRESHOLD = 50


def store_message(message):
    if len(messages) > MESSAGES_THRESHOLD:
        messages.pop(0)
    messages.append(message)

langauages = {
    "model": "",
    "from": "",
    "to": "",
}


@app.route('/result', methods=['POST'])
def post_answer():
    json = request.json
    message = {"option": json["option"], "direction": json["direction"], "text": json["text"]}
    if message["option"] == 'english-input':
        tgt_language = "de"
        text_english = f'>>{tgt_language}<< {message["text"]}'
        translated = model_english.generate(**tokenizer_english.prepare_translation_batch([text_english]))
        message["translation"] = [tokenizer_english.decode(t, skip_special_tokens=True) for t in translated][0]
        store_message(message)
        return message["translation"]

    else:
        tgt_language = "en"
        text_english = f'>>{tgt_language}<< {message["text"]}'
        translated = model_spanish.generate(**tokenizer_spanish.prepare_translation_batch([text_english]))
        message["translation"] = [tokenizer_spanish.decode(t, skip_special_tokens=True) for t in translated][0]
        return message["translation"]


@app.route('/getMessages', methods=['GET'])
def get_messages():
    return {"messages": str(messages)}


@app.route('/postCookie', methods=['POST'])
def post_cookie():
    n = random.choice(["1","2","3"])
    cookies.append(n)
    return {"cookie": n}


@app.route('/getCookies', methods=['GET'])
def get_stored_cookies():
    return {"cookies": str(cookies)}


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8020)
