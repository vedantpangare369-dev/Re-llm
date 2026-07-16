from encode import encode
def input_data():
    with open("inputf","r",encoding="utf-8") as f:
        input_text=f.read()
    tokens=encode(input_text)
    token_len=len(tokens)
    return tokens,token_len
