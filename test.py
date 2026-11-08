nums=[3,1,4,1,5]
print(max(nums),min(nums),sum(nums))
for n in nums:
    print(n*n)
ages={"张三":20,"李四":22,"王五":19}
print(max(ages,key=ages.get))
def get_even(lst):
    return [x for x in lst if x%2==0]
print(get_even([1,2,3,4,5,6]))