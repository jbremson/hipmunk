from flask import Flask, request
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)
CORS(app)

def invalid_response():
    return "Invalid post data. :("

@app.route('/chat/messages', methods=['POST'])
def message():
    if request.method == 'POST':
        vals = json.loads(json.dumps(request.form))
        if not vals.get('action'):
            return invalid_response()

        if vals['action'] == 'join':
            if not vals.get("user_id") and not vals.get("name"):
                return invalid_response()
            out = dict(messages=[dict(type='text',text="Hello {}!".
                                      format(vals['name'].capitalize()))])
            return json.dumps(out)
        elif vals['action'] == 'message':
            pass
        else:
            return invalid_response()


