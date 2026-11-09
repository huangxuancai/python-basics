maps={}
maps["dust2"]=1
print("步骤1:",maps)

maps["dust2"]=99
print("步骤2:",maps)

print("步骤3 前:",maps)
try:
    print(maps["nuke"])
except KeyError as e:
    print("步骤3 崩溃：",e)

if "nuke" in maps:
    maps["nuke"]+=1
else:
    maps["nuke"]=1
print("步骤4:",maps)
maps["inferno"] = maps.get("inferno",0)+1
print("步骤5:",maps)

for _ in range(3):
    maps["inferno"]=maps.get("inferno",0)+1
print("步骤6:",maps)