from reedsolomon.gf_math import gf_poly_eval, gf_pow, gf_mul, gf_poly_scale, gf_inverse, gf_poly_add, gf_poly_mul, gf_poly_div, gf_sub, gf_div


def calc_syndromes(msg, nsym):
    synd = [0] * nsym
    for i in range(0, nsym):
        synd[i] = gf_poly_eval(msg, gf_pow(2,i))
    return [0] + synd 


def find_error_locator(synd, t):
    err_loc = [1]
    old_loc = [1]

    synd_shift = len(synd) - t

    for i in range(0, t):
        K = i+synd_shift
        delta = synd[K]
        for j in range(1, len(err_loc)):
            delta ^= gf_mul(err_loc[-(j+1)], synd[K - j])

        old_loc = old_loc + [0]

        if delta != 0: 
            if len(old_loc) > len(err_loc): 
                new_loc = gf_poly_scale(old_loc, delta)
                old_loc = gf_poly_scale(err_loc, gf_inverse(delta)) 
                err_loc = new_loc

            err_loc = gf_poly_add(err_loc, gf_poly_scale(old_loc, delta))

    while len(err_loc) and err_loc[0] == 0: 
        del err_loc[0] 
    errs = len(err_loc) - 1
    if (errs) * 2 > t:
        raise Exception("Too many errors to correct")

    return err_loc


def find_errors(err_loc, nmess): 
    errs = len(err_loc) - 1
    err_pos = []
    for i in range(nmess):
        if gf_poly_eval(err_loc, gf_pow(2, i)) == 0:
            err_pos.append(nmess - 1 - i)
    if len(err_pos) != errs:
        raise Exception("Too many errors to decode")
    return err_pos


def correct_errata(msg_in, synd, err_pos, err_loc): 
    coef_pos = [len(msg_in) - 1 - p for p in err_pos] 
    product = gf_poly_mul(synd, err_loc)
    divisor = [1] + [0] * len(err_loc)
    _, err_eval = gf_poly_div(product, divisor)
    err_eval = err_eval[::-1]

    error_positions = [] 
    for i in range(0, len(coef_pos)):
        l = 255 - coef_pos[i]
        error_positions.append( gf_pow(2, -l) )

    E = [0] * (len(msg_in)) 
    for index, Xi in enumerate(error_positions):
        Xi_inv = gf_inverse(Xi)
        err_loc_prime_tmp = []
        for j in range(0, len(error_positions)):
            if j != index:
                err_loc_prime_tmp.append(gf_sub(1, gf_mul(Xi_inv, error_positions[j])))

        err_loc_prime = 1
        for coef in err_loc_prime_tmp:
            err_loc_prime = gf_mul(err_loc_prime, coef)

        y = gf_poly_eval(err_eval[::-1], Xi_inv)
        y = gf_mul(gf_pow(Xi, 1), y)
        
        magnitude = gf_div(y, err_loc_prime) 
        E[err_pos[index]] = magnitude 
    result_message = gf_poly_add(msg_in, E)
    return result_message


def rs_decode_msg(msg_in, t):
  msg_out = list(msg_in)
  syndromes = calc_syndromes(msg_out, t)
  if max(syndromes) == 0:
      return msg_out[:-t], []  # no errors

  err_loc = find_error_locator(syndromes[1:], t)
  err_pos = find_errors(err_loc[::-1] , len(msg_out))
  msg_out = correct_errata(msg_out, syndromes[::-1], err_pos, err_loc) 
  return msg_out[:-t], err_pos[::-1]


def decode_chunks(chunks, nsym):
  restored_chunks = []
  errors_per_chunk = []
  for c in chunks:
    corrected_message, err_pos = rs_decode_msg(c, nsym)
    restored_chunks.append(corrected_message)
    errors_per_chunk.append(err_pos)
  return restored_chunks, errors_per_chunk


def restore_text(chunks):
  result_string = ""
  for c in chunks:
    result_string += ''.join([chr(x) for x in c])
  return result_string