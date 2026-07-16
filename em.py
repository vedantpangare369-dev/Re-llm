import random
import numpy as np
from global_variables import vocab_count,dimentions,contex_window
from inputs import input_data
from emb import embeded
embedding_vector=(np.random.randn(vocab_count,dimentions)*0.02).astype(np.float32)
positional_embeddings=(np.random.randn(contex_window,dimentions)*0.02).astype(np.float32)
tokens,token_len=input_data()
x=embeded(embedding_vector,tokens)+positional_embeddings[:len(tokens)]
print(embeded(embedding_vector,tokens),"+",positional_embeddings[:len(tokens)],"=",x,end=" ")



