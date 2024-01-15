def string_to_ord_array(message):
  return [ord(x) for x in message]

def ord_array_to_string(array):
  return "".join(chr(x) for x in array)

def chunk_message(message, k):
  chunks = []
  original_message_chunks = []
  i = 0
  while(i<len(message)):
    if i+k > len(message):
      chunks.append(message[i:len(message)])
      original_message_chunks.append(ord_array_to_string(chunks[len(chunks)-1]))
    else:
      chunks.append(message[i:i+k])
      original_message_chunks.append(ord_array_to_string(chunks[len(chunks)-1]))
    i+=k
  return original_message_chunks, chunks

