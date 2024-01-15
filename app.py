from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from rs import rs_encode, rs_decode, get_encoded_image_chunks
from reedsolomon.rs_encode import rs_generator_poly


app = Flask(__name__)
cors = CORS(app)

prim = 0x11d
n = 255
k = 223
gen_polynomial = rs_generator_poly(n-k)
print()
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@cross_origin()
@app.route("/test", methods=["POST"])
def test():
    text = request.get_json()
    # rs_test(text, rsc)
    result = {"msg": "decoded", "result":191}
    return jsonify(result), 200


@cross_origin()
@app.route("/encode-text", methods=["POST"])
def encode_text():
    request_data = request.get_json()
    original_message_chunks, chunks, encoded_chunks, n = rs_encode(request_data["text"], k, gen_polynomial)
    blocks = []
    for i in range(0, n):
        block = {"original_message": original_message_chunks[i],"chunk": chunks[i],"encoded_chunk": encoded_chunks[i]}
        blocks.append(block)
    return jsonify(blocks), 200


@cross_origin()
@app.route("/decode-text", methods=["POST"])
def decode():
    data = request.get_json()
    decoded_string = rs_decode(data, n-k)
    result = {"decoded_string": decoded_string, "errors_found": 1}
    return jsonify(result), 200


@cross_origin()
@app.route("/encoded-image", methods=["GET"])
def encode_image():
    encoded_image_chunks, length, image_string = get_encoded_image_chunks(k, gen_polynomial)
    return jsonify({
        "encoded_image_chunks": encoded_image_chunks,
        "chunk_number": length,
        "base64": image_string
    }), 200


@cross_origin()
@app.route("/decode-image", methods=["POST"])
def decode_image():
    data = request.get_json()
    decoded_image_base64 = rs_decode(data, n-k)
    return jsonify({"base64":decoded_image_base64}), 200


