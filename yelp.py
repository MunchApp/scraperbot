import requests
import json

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

if __name__ == '__main__':
    main()
