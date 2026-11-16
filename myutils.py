#   1. count_words(text)  ← 从 day6_practice.py C1 搬过来(词频统计)
#   2. format_params(d)   ← 从 day6_practice.py C3 搬过来("&".join 版)
#   3. 文件末尾 if __name__ == "__main__": 自检,两个函数各调用打印一次

def count_words(text):
    ans={}
    for t in text.split():
        ans[t]=ans.get(t,0)+1
    return ans

def format_params(d):
    return "&".join(f"{k}={v}" for k, v in d.items())

if __name__ == "__main__":
    print(count_words("a b a c b a"))                # 期望 {'a': 3, 'b': 2, 'c': 1}
    print(format_params({"name": "张三", "score": 85}))  # 期望 name=张三&score=85