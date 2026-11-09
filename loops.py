for i in range(2,101,2):
    print(i,end=" ")
total = 0
for i in range(1,101):
    total+=i
print(total)

for x in range(1,10):
    for y in range (1,x+1):
        print(f"{y} * {x} = {x*y}",end="   ")
    print()

for i in [3,1,4,1,5,9,2,6]:
    print(i*i,end=" ")
print()

count={}
for c in "hello world":
    count[c]=count.get(c,0)+1
print(count)
    
    




