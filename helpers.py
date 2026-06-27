def get_reverse_merge(merge):
    reverse_merge={}
    for key,value in merge.items():
        reverse_merge[value]=key
    return reverse_merge
def get_stats(tokens):
    freq = {}
    for i in range(len(tokens) - 1):
        pair = (tokens[i], tokens[i + 1])
        freq[pair] = freq.get(pair, 0) + 1
    return freq