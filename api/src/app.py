from api.src import app
from api.src.controllers import cookies_contoller, next_word_predictor_controller, message_controller


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8020)
