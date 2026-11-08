import random
answer = random.randint(1,100)
count = 0
print("我想了一个1-100的数字，你猜猜看")
while True:
    if count>7:
            print("次数超过7,你输了")
            break
    guess=int(input("请输入你的数字："))
    count+=1
    
    if guess>answer:
        print("大了")
    elif guess<answer:
        print("小了")
    else:
        print(f"猜对了，你用了{count}次")
        break