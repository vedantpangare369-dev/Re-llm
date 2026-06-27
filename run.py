with open("inputfile.txt","r",encoding="utf-8") as f:
    input_text = f.read()
from encode import  encode
from decode import decode


print(decode(encode(input_text)))
