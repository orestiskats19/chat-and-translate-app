from api.src import cookies
from api.src import app
from flask import request
import uuid


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
