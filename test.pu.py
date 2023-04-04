import json

with open("dataBase.json") as file:
    new_dict = json.load(file)

ser_id = "189438743"

if ser_id in new_dict:
    print("Yes")
else:
    print("No")