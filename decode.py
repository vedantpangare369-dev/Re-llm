import pickle
with open("merges.pickle","br") as f:
    merges=pickle.load(f)
def decode(vocab):
    result=b""
    for token in vocab:
        if(token<256):
            result+=bytes([token])
        else:
             result+=decode_text_helper(token)
    return result.decode("utf-8")
def decode_text_helper(p):
    
    print(type(p), p)
    if p<256:
        return bytes([p])
    
    pair=merges[p]
    return decode_text_helper(pair[0])+ decode_text_helper(pair[1])