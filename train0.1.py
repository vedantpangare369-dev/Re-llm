import heapq
import pickle
import time

from decode import decode

# from encode import encode
vocab_count=255
vocab=list(range(256))
merges={}
class node:
    def __init__(self, token):
        self.token = token
        self.next = None
        self.prev = None
        self.occ_idx=0
        self.alive= True


class ll:
    def __init__(self,tokens):
        self.head = node(tokens[0])
        self.tail = None
        self.freq={}
        self.occ={}
        self.heap=[]
        self.a=[]
        curr = self.head         
           
      
        for token in tokens[1:]:
            
            new = node(token)
        

            curr.next = new
            new.prev = curr
            pair=(curr.token,token)
            self.freq[pair]=self.freq.get(pair,0)+1
            if self.occ.setdefault(pair,[]):
                self.occ[pair].append(curr)
                curr.occ_idx=len(self.occ[pair])-1
            else:
                self.occ[pair]=[]
                self.occ[pair].append(curr)
                curr.occ_idx=0

            curr = new
        for pair in self.freq:
            self.heap_push(pair)

        self.tail = curr
       
       

    def print_list(self):
        curr = self.head          # was: head

     
        
        self.a=[]
      
        while curr:
            self.a.append(curr.token)
            curr=curr.next
          
        

    def print_list_reverse(self):
        curr = self.tail          # was: head

      
        print("None"," <-> ",end=" ")
        while curr:
            print(curr.token," <-> ",end=" ")
            curr=curr.prev
        print("None",end=" ")
    def delete(self,node):
        if self.lonely(node):
            return
        p=node
        if not p.next:
            self.tail=p.prev
            p.prev.next=None
            p.prev=None
        elif not p.prev:
            self.head=p.next
            p.next.prev=None
            p.next=None
        else:
            p.prev.next=p.next
            p.next.prev=p.prev
            p.next=None
            p.prev=None
        p.alive=False  
        
    def heap_push(self, pair):
        if pair in self.freq:
            heapq.heappush(self.heap, (-self.freq[pair], pair))
    def update_occ(self, left, idx):
        A = left
        B = left.next
        X = None
        Y = None

        if A.prev:
            X = A.prev
        if B.next:
            Y = B.next

        

       
        if X:
            merge_left = (X.token, A.token)

            if merge_left in self.occ:
                bucket = self.occ[merge_left]
                # occ_idx can go stale if merge_left and merge_right alias to
                # the same bucket (X.token==B.token and A.token==Y.token) -
                # only trust the index if it still points at X itself.
                if X.occ_idx < len(bucket) and bucket[X.occ_idx] is X:
                    bucket[X.occ_idx] = bucket[-1]
                    bucket[X.occ_idx].occ_idx = X.occ_idx
                    bucket.pop()
                elif X in bucket:
                    bucket.remove(X)

                if len(bucket) == 0:
                    del self.occ[merge_left]

            new_left = (X.token, idx)
            self.occ.setdefault(new_left, []).append(X)
            X.occ_idx = len(self.occ[new_left]) - 1

        if Y:
            merge_right = (B.token, Y.token)
            if merge_right in self.occ:
                bucket = self.occ[merge_right]
                if B.occ_idx < len(bucket) and bucket[B.occ_idx] is B:
                    bucket[B.occ_idx] = bucket[-1]
                    bucket[B.occ_idx].occ_idx = B.occ_idx
                    bucket.pop()
                elif B in bucket:
                    bucket.remove(B)

                if merge_right in self.occ and len(self.occ[merge_right]) == 0:
                    del self.occ[merge_right]

            new_right = (idx, Y.token)
            self.occ.setdefault(new_right, []).append(A)
            A.occ_idx = len(self.occ[new_right]) - 1
    def update_freq(self, left, idx):
        A = left
        B = left.next
        X = None
        Y = None

        if A.prev:
            X = A.prev
        if B.next:
            Y = B.next

        merge_pair = (A.token, B.token)

        if merge_pair in self.freq:
            self.freq[merge_pair] -= 1

            if self.freq[merge_pair] == 0:
                del self.freq[merge_pair]
            else:
                self.heap_push(merge_pair)

        if X:
            left_pair = (X.token, A.token)

            if left_pair in self.freq:
                self.freq[left_pair] -= 1

                if self.freq[left_pair] == 0:
                    del self.freq[left_pair]
                else:
                    self.heap_push(left_pair)

        if Y:
            right_pair = (B.token, Y.token)

            if right_pair in self.freq:
                self.freq[right_pair] -= 1

                if self.freq[right_pair] == 0:
                    del self.freq[right_pair]
                else:
                    self.heap_push(right_pair)

        if Y:
            new_right = (idx, Y.token)
            self.freq[new_right] = self.freq.get(new_right, 0) + 1
            self.heap_push(new_right)

        if X:
            new_left = (X.token, idx)
            self.freq[new_left] = self.freq.get(new_left, 0) + 1
            self.heap_push(new_left)
    def train(self,target,merges):
        global vocab_count
        start = time.perf_counter()
        while vocab_count < target:
            # print("HEAP SIZE", len(self.heap))
            if not self.heap:
                print(f"Stopped early at vocab_count={vocab_count}: "
                      f"no more mergeable pairs left in the input.")
                break
            count, pair = heapq.heappop(self.heap)
            if vocab_count % 100 == 0:
                elapsed = time.perf_counter() - start
                done = vocab_count - 255
                speed = done / elapsed
                remaining = target - vocab_count
                eta = remaining / speed

                print(
                 f"\rMerge: {done:5d} | "
                 f"Speed: {speed:8.1f} merges/s | "
                    f"ETA: {eta:6.1f}s",
                end=""
                 )

                print()
          
           
            
            
            # print("PAIR:", pair)
            # print("COUNT:", count)
            if pair not in self.freq:
                continue
            
            if -count != self.freq[pair]:
                continue
            idx = new_token(pair,merges)
            # print("BEST", pair, self.freq[pair])
            for node in self.occ[pair][:]:
                

                
                
                if node.token != pair[0]:
                    continue
                
                
                if not node.alive:
                    continue
                if node.next is None:
                    continue
                if node.next.alive == False:
                    continue
                if node.next.token != pair[1]:
                    continue
                
                # print(node.token, node.next.token)

                self.merge(node,idx)
            # print("FAST", pair)
               
            del self.occ[pair]

        
    def merge(self,left,idx):
        A = left
        B = left.next
        pair=merges[idx]
        # print("MERGING")
        # print("A", A.token)
        # print("B", B.token)
        # idx = new_token(pair,merges)
        # print("NEW", idx)
       

        self.update_occ(left, idx)
        self.update_freq(left, idx)
        
        A.token = idx

        if A and B:
            self.delete(B)



            
    def lonely(self,node):
        if not node.next and not node.prev:
            return True
        return False  
    

def new_token(pair, merges):
    global vocab_count
    vocab_count += 1
    vocab.append(vocab_count)
    merges[vocab_count] = pair
    return vocab_count
def ok(head):
    i=0
    tokens=[]
    curr=head
    while curr:
        tokens.append(curr.token)
        curr=curr.next
        i+=1
    return i,tokens
        
# ---------------- MAIN ---------------- #
with open("inputfile.txt", "r", encoding="utf-8") as f:                 
    text = f.read()


tokens = list(text.encode("utf-8"))
a=len(tokens)


if tokens:

    l = ll(tokens)
if not l.lonely(l.head):                
    # l.print_list()
    start = time.perf_counter()
    l.train(50000+255,merges)
    # l.print_list()
    # k=l.heap
    # print(k)
    # k,new_tokens=ok(l.head)
    # old_tokens=add_tokens(5,tokens,merges)
    l.print_list()
   
    with open("merges.pickle","bw") as f:
        pickle.dump(merges,f)
    print("heap:", len(l.heap))
    print("freq:", len(l.freq))
    print("occ:", len(l.occ))
    print("vocab_count:", vocab_count)
    b=l.a
    # print(decode(a,merges))
    # print(l.head)            # is this literally None, or a node object?
    # print(l.head.token if l.head else "HEAD IS NONE")
    elapsed = time.perf_counter() - start


    print(f"Time: {elapsed:.3f}s")
    print("number of chacters",a)
    
    