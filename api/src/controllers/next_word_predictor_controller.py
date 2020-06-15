from api.src import next_token_model_wrapper
from flask import request
from api.src import app


@app.route('/next_word_predictor', methods=['POST'])
def post_next_word():
    input_json = request.json
    if input_json["text"] and not input_json["text"].startswith(" "):
        tokens = next_token_model_wrapper.next_word_predictor(input_json["text"])
        return {"tokens": tokens}
    return {"tokens": []}