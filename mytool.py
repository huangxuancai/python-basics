#   1. 顶层一句: print(f"[mytool] 顶层执行, __name__={__name__}")
#   2. 函数 double(x): 返回 x*2
#   3. if __name__ == "__main__": 守卫里 print("直接运行自检:", double(21))
print(f"[mytool] 顶层执行, __name__={__name__}")

def double(x):
    return x*2

if __name__ == "__main__":
    print("直接运行自检:", double(21))