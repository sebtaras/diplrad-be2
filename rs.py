from reedsolomon.util import string_to_ord_array, chunk_message
from reedsolomon.rs_encode import encode_chunks
from reedsolomon.rs_decode import decode_chunks, restore_text
import base64


def rs_encode(message, k, gen_polynomial):
  # print("message", message)
  prepared_message = string_to_ord_array(message)
  # print("prepared message", prepared_message)
  original_message_chunks, chunks = chunk_message(prepared_message, k)
  # print("chunks", chunks)
  # print("original message_chunks", original_message_chunks)
  encoded_chunks = encode_chunks(chunks, gen_polynomial)
  # print("encoded chunks", encoded_chunks)
  return original_message_chunks, chunks, encoded_chunks, len(original_message_chunks)


def rs_decode_image(encoded_chunks, nsym):
  errors_found = 0
  total_symbols = 0
  decoded_chunks, err_pos = decode_chunks(encoded_chunks, nsym)
  for i in range(0, len(decoded_chunks)):
    total_symbols += len(decoded_chunks[i])
    errors_found += len(err_pos[i])
  result_string = restore_text(decoded_chunks)
  return result_string, errors_found, round((errors_found / total_symbols)*100,2).__str__()


def rs_decode_text(encoded_chunks, nsym):
  result_chunks = []
  decoded_chunks, err_pos = decode_chunks(encoded_chunks, nsym)
  for i in range(0, len(decoded_chunks)):
    result_chunks.append({"text": restore_text([decoded_chunks[i]]), "errored_symbols": err_pos[i]})

  result_string = restore_text(decoded_chunks)
  return result_string, result_chunks


def get_encoded_image_chunks(k, gen_polynomial):
  with open("./reedsolomon/dvds.png", "rb") as image:
    image_binary = image.read()
    image_string = base64.b64encode(image_binary).decode("utf-8")
    image_ord_string = string_to_ord_array(image_string)

    _, chunks = chunk_message(image_ord_string, k)
    encoded_chunks = encode_chunks(chunks, gen_polynomial)

    return encoded_chunks, len(encoded_chunks), image_string