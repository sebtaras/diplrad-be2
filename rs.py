from reedsolomon.util import string_to_ord_array, chunk_message
from reedsolomon.rs_encode import encode_chunks
from reedsolomon.rs_decode import decode_chunks, restore_text
import base64


def rs_encode(message, k, gen_polynomial):
  print("message", message)
  prepared_message = string_to_ord_array(message)
  print("prepared message", prepared_message)
  original_message_chunks, chunks = chunk_message(prepared_message, k)
  print("chunks", chunks)
  print("original message_chunks", original_message_chunks)
  encoded_chunks = encode_chunks(chunks, gen_polynomial)
  print("encoded chunks", encoded_chunks)
  return original_message_chunks, chunks, encoded_chunks, len(original_message_chunks)


def rs_decode(encoded_chunks, nsym):
  print("encoded chunks:", encoded_chunks)
  decoded_chunks = decode_chunks(encoded_chunks, nsym)
  result = restore_text(decoded_chunks)
  print("result", result)
  return result


def get_encoded_image_chunks(k, gen_polynomial):
  with open("./reedsolomon/dvds.png", "rb") as image:
    image_binary = image.read()
    image_string = base64.b64encode(image_binary).decode("utf-8")
    image_ord_string = string_to_ord_array(image_string)
    print(image_string)
    print(image_ord_string, len(image_ord_string))

    _, chunks = chunk_message(image_ord_string, k)
    encoded_chunks = encode_chunks(chunks, gen_polynomial)

    # for c in chunks:
      # encoded_image_chunk = encode_chunks(c, gen_polynomial)
      # encoded_chunks.append(encoded_image_chunk)

    print(encoded_chunks, len(encoded_chunks))

    return encoded_chunks, len(encoded_chunks), image_string