import json



d_py = {'key1':'val1','key2':'val2'}

for key, value in d_py.items():
    print(key, '->', value)

out_file = open("test1.json", "w") 
json.dump(d_py, out_file, indent = 4, sort_keys = False) 
out_file.close() 

with open("test1.json") as f:
    data = json.load(f)

print(data)
#j_c = json.loads(data)
#print(j_c)
for key, value in data.items():
    print(key, '->', value)


with open("db_config.json") as f:
    data = json.load(f)

print(data)

for key, value in data.items():
    print(key, '->', value)

l_s = "b'{\n    "db_username":"postgres",\n    "db_password":"dashboard",\n    "db_name":"lambda-test-db",\n    "db_endpoint":"lambda-test.cyb3keo6utm7.us-east-1.rds.amazonaws.com",\n    "schema":"lambda-test",\n    "table":"badgedata"\n}'"

print(l_s)