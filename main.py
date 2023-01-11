import requests
import json

# Test via console
response = requests.get('https://api.fbi.gov/@wanted?pageSize=50&page=4&sort_on=modified&sort_order=desc'
                        )
data = json.loads(response.content)
print(data['total'])

for i in range(50):
    print(f"Suspect number {i+1}: \n {data['items'][i]['title']}")

sus_number = int(input("Get suspect: "))

print("\n--------")
print(f"This is {data['items'][sus_number-1]['title']}")