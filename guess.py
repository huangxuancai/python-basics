import random
answer = random.randint(1,100)
count = 0
print("我想了一个1-100的数字，你猜猜看")
while True:
    if count>=7:
            print("7 次机会用完了")
            break
    while True:
        raw = input("请输入你的数字：")
        try:
            guess=int(raw)
            break
        except ValueError:
            print("请输入数字！")
    
    count+=1
        
    if guess>answer:
        print("大了")
    elif guess<answer:
        print("小了")
    else:
        print(f"猜对了，你用了{count}次")
        ans = input("你还想玩吗？")
        
        if ans == "yes":
            answer = random.randint(1,100)
            count = 0
            continue
        elif ans == "no":
            break

    
    