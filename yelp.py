import requests

print("Hello")

print("__name__ value: ", __name__)

def main():
    print("python main function...")
    response = requests.get("https://munch-server.herokuapp.com/contributors")
    print(response.status_code)

if __name__ == '__main__':
    main()

