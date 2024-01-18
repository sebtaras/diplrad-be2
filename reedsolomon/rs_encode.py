from reedsolomon.gf_math import gf_poly_div, gf_poly_mul, gf_pow


def rs_generator_poly(t):
    g = [1]
    for i in range(0, t):
        g = gf_poly_mul(g, [1, gf_pow(2, i)])
    return g


def rs_encode_msg(msg_in, gen):
    _, remainder = gf_poly_div(msg_in + [0] * (len(gen)-1), gen)
    msg_out = msg_in + remainder
    return msg_out


def encode_chunks(chunks, gen_polynomial):
  encoded_chunks = []
  for c in chunks:
    m = rs_encode_msg([x for x in c], gen_polynomial)
    encoded_chunks.append(m)
  return encoded_chunks