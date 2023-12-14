from reedsolo import RSCodec, ReedSolomonError
from util import prepare_string_for_encoding
import codecs

def rs_encode(text, rsc: RSCodec): 
  string_bytearray = prepare_string_for_encoding(text)
  res = rsc.encode(string_bytearray)
  # res = rsc.encode([1,2,3,4])
  return res

def rs_decode(text, rsc: RSCodec):
  res = rsc.decode(text)
  return res

def rs_test(text,rsc: RSCodec):
  print("text:", text)
  # print("text.encode:", text.encode("utf-8"))
  print("bytearray(text.encode):", prepare_string_for_encoding(text))
  # print("rsc.encode(text.encode)", rsc.encode(text.encode))
  encoded = rsc.encode(prepare_string_for_encoding(text))
  print("ENCODED:", encoded)
  print("ENCODED str:", encoded.__str__())
  # print("ENCODED decode utf8:", encoded.decode('utf-8'))
  dec = rsc.decode(rsc.encode(prepare_string_for_encoding(text)))
  print("RSC[0] DECODED:", dec[0])
  result_string = dec[0].decode('utf-8')
  print("decode to utf8: ", result_string)
  print("other decoded data 1 -> this is the input", dec[1])
  print("other decoded data 2 -> list of positions of the error data", dec[2])