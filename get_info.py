import requests
import json
import sys
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

def putAllInDb(input, postlink):
    businessList = input['businesses']
    listlen = len(businessList)
    for b in businessList:

        notCredible = False

        if 'name' in b:
            Name = b['name']

        if 'id' in b:
            id = b['id']

        Address = "No address listed..."
        if 'location' in b:
            address = b['location']['display_address']
            if len(address) >= 2:
                Address = address[0] + '\n' + address[1]
            else:
                notCredible = True

        if 'phone' in b:
            PhoneNumber = b['phone']

        baseURL = 'https://api.yelp.com/v3/businesses/'
        urlSearchByID = 'https://api.yelp.com/v3/businesses/' + id

        req = requests.get(urlSearchByID, headers=headers)
        businessJSON = req.json()
        #fieldlist = businessJSON['search']
        #jprint(req.json())

        mondayStart = "99:99"
        mondayEnd = "99:99"
        tuesdayStart = "99:99"
        tuesdayEnd = "99:99"
        wednesdayStart = "99:99"
        wednesdayEnd = "99:99"

        thursdayStart = "99:99"
        thursdayEnd = "99:99"
        fridayStart = "99:99"
        fridayEnd = "99:99"
        saturdayStart = "99:99"
        saturdayEnd = "99:99"
        sundayStart = "99:99"
        sundayEnd = "99:99"

        i = 0
        if 'hours' in businessJSON:
            for day in businessJSON['hours'][0]['open']:
                dayIndex = day['day']
                if dayIndex == 0:
                    mondayStart = businessJSON['hours'][0]['open'][i]['start']
                    mondayStart = mondayStart[:2] + ":" + mondayStart[2:]
                    mondayEnd = businessJSON['hours'][0]['open'][i]['end']
                    mondayEnd = mondayEnd[:2] + ":" + mondayEnd[2:]
                if dayIndex == 1:
                    tuesdayStart = businessJSON['hours'][0]['open'][i]['start']
                    tuesdayStart = tuesdayStart[:2] + ":" + tuesdayStart[2:]
                    tuesdayEnd = businessJSON['hours'][0]['open'][i]['end']
                    tuesdayEnd = tuesdayEnd[:2] + ":" + tuesdayEnd[2:]
                if dayIndex == 2:
                    wednesdayStart = businessJSON['hours'][0]['open'][i]['start']
                    wednesdayStart = wednesdayStart[:2] + ":" + wednesdayStart[2:]
                    wednesdayEnd = businessJSON['hours'][0]['open'][i]['end']
                    wednesdayEnd = wednesdayEnd[:2] + ":" + wednesdayEnd[2:]
                if dayIndex == 3:
                    thursdayStart = businessJSON['hours'][0]['open'][i]['start']
                    thursdayStart = thursdayStart[:2] + ":" + thursdayStart[2:]
                    thursdayEnd = businessJSON['hours'][0]['open'][i]['end']
                    thursdayEnd = thursdayEnd[:2] + ":" + thursdayEnd[2:]
                if dayIndex == 4:
                    fridayStart = businessJSON['hours'][0]['open'][i]['start']
                    fridayStart = fridayStart[:2] + ":" + fridayStart[2:]
                    fridayEnd = businessJSON['hours'][0]['open'][i]['end']
                    fridayEnd = fridayEnd[:2] + ":" + fridayEnd[2:]
                if dayIndex == 5:
                    saturdayStart = businessJSON['hours'][0]['open'][i]['start']
                    saturdayStart = saturdayStart[:2] + ":" + saturdayStart[2:]
                    saturdayEnd = businessJSON['hours'][0]['open'][i]['end']
                    saturdayEnd = saturdayEnd[:2] + ":" + saturdayEnd[2:]
                if dayIndex == 6:
                    sundayStart = businessJSON['hours'][0]['open'][i]['start']
                    sundayStart = sundayStart[:2] + ":" + sundayStart[2:]
                    sundayEnd = businessJSON['hours'][0]['open'][i]['end']
                    sundayEnd = sundayEnd[:2] + ":" + sundayEnd[2:]
                i += 1

        Hours = [[sundayStart, sundayEnd],
                 [mondayStart, mondayEnd],
                 [tuesdayStart, tuesdayEnd],
                 [wednesdayStart, wednesdayEnd],
                 [thursdayStart, thursdayEnd],
                 [fridayStart, fridayEnd],
                 [saturdayStart, saturdayEnd]]

        if 'photos' in businessJSON:
            Photos = businessJSON['photos']

        Tags = generateCategories(businessJSON['categories'])
        Description = "this is an example description..."
        Location = [businessJSON['coordinates']['latitude'], businessJSON['coordinates']['longitude']]
        Website = businessJSON['url']

        returnDictionary = {
            "name": Name,
            "address":Address,
            "location":Location,
            "hours":Hours,
            "photos":Photos,
            "website":Website,
            "phoneNumber":PhoneNumber,
            "description":Description,
            "tags":Tags
        }

        useragentheader = {'User-agent': 'MunchCritic/1.0'}

        if not notCredible:
            r = requests.post(postlink, headers=useragentheader, json=returnDictionary)
            print("Adding " + Name + " to the database...")
            if r.status_code == 200:
                print("Adding successful!")
            else:
                print("Could not add " + Name + " to the database.")

def getYelpData(inputLink):
    url = 'https://api.yelp.com/v3/businesses/search'

    # In the dictionary, term can take values like food, cafes or businesses like McDonalds
    params = {'term': 'food truck', 'location': 'Austin'}
    req = requests.get(url, params=params, headers=headers)
    print('The status code is {}'.format(req.status_code))
    #jprint(req.json())
    yelpBusinesses = req.json()

    #name, address, hours, photos (array of URL), website, phone, desc, tags
    putAllInDb(yelpBusinesses, inputLink)

# if __name__ == '__main__':
#     print("Running script: " + sys.argv[0] + "...")
#     if len(sys.argv) > 1:
#         getYelpData(sys.argv[1])
# #         http://munch-server.herokuapp.com/foodtrucks
#     else:
#         getYelpData('http://localhost/foodtrucks')


if __name__ == '__main__':
    print("Starting scraperbot... \nPlease enter a number to get started: \n   1. Update Yelp\n   2. Update Google\n   3. Add food truck by name\n")
    command = input("")

    if command in ["1"]:
        print("You chose: Update Yelp")
    if command in ["2"]:
        print("You chose: Update Google")
    if command in ["3"]:
        print("You chose: Add food truck by name...")

    print("\nGotcha. Do you want to update the localhost or the herokuapp databases?\n   1. localhost\n   2. heroku\n")
    server = input("")

    if server in ["1"]:
        print("Running on localhost...")

        if command in ["1"]:
            getYelpData('http://localhost/foodtrucks')
        if command in ["2"]:
            print("You chose: Update Google")
        if command in ["3"]:
            print("You chose: Add food truck by name...")

    elif server in ["2"]:
        print("Running on heroku...")

        if command in ["1"]:
            getYelpData('http://munch-server.herokuapp.com/foodtrucks')
        if command in ["2"]:
            print("You chose: Update Google")
        if command in ["3"]:
            print("You chose: Add food truck by name...")