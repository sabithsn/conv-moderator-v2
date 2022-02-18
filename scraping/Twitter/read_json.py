import json

f = open ("data.json")
json_response = json.load (f)
for j in json_response:
	print (j)
print(json.dumps(json_response, indent=4, sort_keys=True))
f.close()
