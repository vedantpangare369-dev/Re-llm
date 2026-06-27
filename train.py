import pickle
with open("testdata.txt","r",encoding="utf-8") as f:
    train_text = f.read()
tokens=train_text.encode("utf-8")
tokens=list(tokens)
merges={}
vocab=list(range(256))
vocab_count=255

def best_pair(tokens):
    freq = {}

    for i in range(len(tokens) - 1):
        pair = (tokens[i], tokens[i + 1])
        freq[pair] = freq.get(pair, 0) + 1

   
    return max(freq,key=lambda x:freq[x])
def merge(pair, tokens, merges):
    idx = new_token(pair,merges)

    

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
def new_token(pair,merges):
    global vocab_count
    vocab_count+=1
    vocab.append(vocab_count)
    merges[vocab_count]=pair
    return vocab_count
def add_tokens(x,tokens,merges):#O(m)



    for i in range(x):
        pair = best_pair(tokens)

        if i % 100 == 0:
            print(
                "Merge:", i,
                "Tokens:", len(tokens)
                 )

        tokens = merge(pair,tokens,merges)

    return tokens
add_tokens(500,tokens,merges)

with open("merges.pickle","bw") as f:
    pickle.dump(merges,f)
    print(vocab)


