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

def generateCategories(categoriesList):
    returnArray = []
    for c in categoriesList:
        returnArray.append(c['title'])
    return returnArray

def putAllInDb(input):
    businessList = input['businesses']
    listlen = len(businessList)
    for b in businessList:
        Name = b['name']
        id = b['id']

        #todo: join the array together with a newline
        address = b['location']['display_address']
        Address = address[0] + '\n' + address[1]
        PhoneNumber = b['phone']

        baseURL = 'https://api.yelp.com/v3/businesses/'
        urlSearchByID = 'https://api.yelp.com/v3/businesses/' + id

        req = requests.get(urlSearchByID, headers=headers)
        businessJSON = req.json()
        #fieldlist = businessJSON['search']
        jprint(req.json())

        #calculating hours
        sundayStart = businessJSON['hours'][0]['open'][6]['start']
        sundayEnd = businessJSON['hours'][0]['open'][6]['end']
        mondayStart = businessJSON['hours'][0]['open'][0]['start']
        mondayEnd = businessJSON['hours'][0]['open'][0]['end']
        tuesdayStart = businessJSON['hours'][0]['open'][1]['start']
        tuesdayEnd = businessJSON['hours'][0]['open'][1]['end']
        wednesdayStart = businessJSON['hours'][0]['open'][2]['start']
        wednesdayEnd = businessJSON['hours'][0]['open'][2]['end']
        thursdayStart = businessJSON['hours'][0]['open'][3]['start']
        thursdayEnd = businessJSON['hours'][0]['open'][3]['end']
        fridayStart = businessJSON['hours'][0]['open'][4]['start']
        fridayEnd = businessJSON['hours'][0]['open'][4]['end']
        saturdayStart = businessJSON['hours'][0]['open'][5]['start']
        saturdayEnd = businessJSON['hours'][0]['open'][5]['end']

        Hours = [[sundayStart, sundayEnd],
                 [mondayStart, mondayEnd],
                 [tuesdayStart, tuesdayEnd],
                 [wednesdayStart, wednesdayEnd],
                 [thursdayStart, thursdayEnd],
                 [fridayStart, fridayEnd],
                 [saturdayStart, saturdayEnd]]

        Photos = businessJSON['photos']
        Tags = generateCategories(businessJSON['categories'])
        Description = "this is an example description..."
        Location = [businessJSON['coordinates']['latitude'], businessJSON['coordinates']['longitude']]
        Website = businessJSON['url']

        returnDictionary = {
            "Name": Name,
            "Address":Address,
            "Location":Location,
            "Hours":Hours,
            "Photos":Photos,
            "Website":Website,
            "PhoneNumber":PhoneNumber,
            "Description":Description,
            "Tags":Tags
        }

        dictJSON = json.dumps(returnDictionary)

        print()


def main():
    url = 'https://api.yelp.com/v3/businesses/search'

    # In the dictionary, term can take values like food, cafes or businesses like McDonalds
    params = {'term': 'food truck', 'location': 'Austin'}
    req = requests.get(url, params=params, headers=headers)
    print('The status code is {}'.format(req.status_code))
    jprint(req.json())
    yelpBusinesses = req.json()

    #name, address, hours, photos (array of URL), website, phone, desc, tags
    putAllInDb(yelpBusinesses)

if __name__ == '__main__':
    main()
