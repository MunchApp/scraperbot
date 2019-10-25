import requests
import json
from yelp.client import Client

print("Hello")
print("__name__ value: ", __name__)

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def main():
    print("python main function...")
    response = requests.get("https://munch-server.herokuapp.com/contributors")
    jprint(response.json())
    print(response.status_code)
    result = json.loads(response)
    print(result)

    MY_API_KEY = "LkR2_IcEI64ibyBqKbF5QSX1fIIHbut01A-F2lOAPcic8XlA-gMnn0R2s79gy3LMLUYiEPWOqUpqqkVORbxF94HljLFUocMvLYXTNZMuQcxGuf58lxjZIQg8C3WyXXYx"  # Replace this with your real API key
    client = Client(MY_API_KEY)

    #client = getClient("yelp")

    business_response = client.business.get_by_id('four seasons austin')

    print(business_response)

if __name__ == '__main__':
    main()
