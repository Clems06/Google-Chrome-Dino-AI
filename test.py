import math

class Ob:
    def __init__(self, id):
        self.id=id

def sort(lis,leng):
    sample=lis[::-1]
    sortd=[]
    num=0
    pre=-1
    for obj,score in sample:
        if score!=pre:
            pre=score
            sortd.append((obj,score//100))
            num+=1
            if num==leng:
                return sortd


a=[(Ob(1),100),(Ob(2),200),(Ob(2),600),(Ob(3),600),(Ob(4),700),(Ob(5),1000),(Ob(7),1000)]
for i,score in sort(a,5):
    print(i.id,score)
