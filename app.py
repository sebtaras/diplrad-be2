from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from reedsolo import RSCodec
from rs import rs_encode, rs_decode, rs_test

app = Flask(__name__)
cors = CORS(app)
rsc = RSCodec(10)
rsc.decode
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@cross_origin()
@app.route("/encode", methods=["POST"])
def encode():
    text = request.get_json()
    encoded = rs_encode(text, rsc)
    result = {"result": "".join(chr(i) for i in encoded)}
    return jsonify(result), 200


@cross_origin()
@app.route("/decode", methods=["POST"])
def decode():
    data = dict(request.data)
    print(data)
    result = {"msg": "decoded", "result":191}
    return jsonify(result), 200

@app.route("/test", methods=["POST"])
def test():
    text = request.get_json()
    rs_test(text, rsc)
    result = {"msg": "decoded", "result":191}
    return jsonify(result), 200