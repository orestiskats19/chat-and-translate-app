from flask import Flask, request, render_template
from transformers import MarianMTModel,MarianTokenizer
from api import model_english,model_spanish, tokenizer_english,tokenizer_spanish
from flask_cors import CORS

app = Flask(__name__, static_folder='../frontend/build')
CORS(app)


@app.route('/result', methods=['POST'])
def post_answer():
    json = request.json
    print(json)
    option = json["option"]
    print(option)
    text = json["question"]
    if option == 'english-input':
        tgt_language = "es"
        text_english = f'>>{tgt_language}<< {text}'
        print(text_english)
        translated = model_english.generate(**tokenizer_english.prepare_translation_batch([text_english]))
        return [tokenizer_english.decode(t, skip_special_tokens=True) for t in translated][0]

    else:
        tgt_language = "en"
        text_english = f'>>{tgt_language}<< {text}'
        translated = model_spanish.generate(**tokenizer_spanish.prepare_translation_batch([text_english]))
        return [tokenizer_spanish.decode(t, skip_special_tokens=True) for t in translated][0]

    return None



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8020)