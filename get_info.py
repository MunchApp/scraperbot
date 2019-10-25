import requests
import json
from secrets import returnYelpApi

from yelp.client import Client

import get_info


api_key = returnYelpApi()
headers = {'Authorization': 'Bearer %s' % api_key}

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def main():
    url = 'https://api.yelp.com/v3/businesses/search'

    # In the dictionary, term can take values like food, cafes or businesses like McDonalds
    params = {'term': 'food truck', 'location': 'Austin'}
    req = requests.get(url, params=params, headers=headers)
    print('The status code is {}'.format(req.status_code))
    jprint(req.json())


if __name__ == '__main__':
    main()
