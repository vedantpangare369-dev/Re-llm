import pickle
with open("merges.pickle","br") as f:
    merges=pickle.load(f)
from helpers import get_stats,get_reverse_merge
def merge_apply(pair,tokens,idx):        
   

    i = 0
    new_tokens = []

    while i < len(tokens):

        if (
            i < len(tokens) - 1
            and tokens[i] == pair[0]
            and tokens[i + 1] == pair[1]
        ):
            new_tokens.append(idx)
            i += 2

        else:
            new_tokens.append(tokens[i])
            i += 1

    return new_tokens
def encode(encoded_text):
    reverse_merge=get_reverse_merge(merges)
    encoded_text=list(encoded_text.encode("utf-8"))
    while True:
        stats=get_stats(encoded_text)
        if not stats:
            break
        pair=min(stats,key=lambda x: reverse_merge.get(x,float("inf")))
        if pair not in reverse_merge:
            break
        idx=reverse_merge[pair]
        encoded_text=merge_apply(pair,encoded_text,idx)

    return encoded_text    