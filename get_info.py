import requests
import json
from secrets import returnYelpApi
from secrets import returnPlacesApi
import pytz
from datetime import datetime

yelp_key = returnYelpApi()
headers = {'Authorization': 'Bearer %s' % yelp_key}
places_key = returnPlacesApi()

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def generateCategories(categoriesList):
    returnArray = []
    for c in categoriesList:
        returnArray.append(c['title'])
    return returnArray

def putOneInDb(b, postlink):
    notCredible = False
    useragentheader = {'User-agent': 'MunchCritic/1.0'}
    reviewURL = postlink[:-10] + "reviews"

    if 'name' in b:
        Name = b['name']
    else:
        print("ERROR: No name for the food truck. Most likely API failure.")
        return

    print("Adding " + Name + " to the database...")

    if 'id' in b:
        id = b['id']

    Address = "No address listed..."
    if 'location' in b:
        address = b['location']['display_address']
        if len(address) >= 2:
            Address = address[0] + '\n' + address[1]
        else:
            notCredible = True
            print("ERROR: Did not add " + " to the database...")

    foodtruckexistsparams = {'name': Name}
    r = requests.get(postlink, foodtruckexistsparams)
    response = r.json()

    if len(response) > 0:
        for conflict in response:
            conAddress = conflict['address']
            if conAddress == Address:
                print("ERROR: Food truck already exists in database.")
                return

    if 'phone' in b:
        PhoneNumber = b['phone']

    baseURL = 'https://api.yelp.com/v3/businesses/'
    urlSearchByID = 'https://api.yelp.com/v3/businesses/' + id
    urlSearchReviews = 'https://api.yelp.com/v3/businesses/' + id + '/reviews'

    req = requests.get(urlSearchByID, headers=headers)
    businessJSON = req.json()

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
    Description = ""
    Location = [businessJSON['coordinates']['latitude'], businessJSON['coordinates']['longitude']]
    Website = businessJSON['url']

    returnDictionary = {
        "name": Name,
        "address": Address,
        "location": Location,
        "hours": Hours,
        "photos": Photos,
        "website": Website,
        "phoneNumber": PhoneNumber,
        "description": Description,
        "tags": Tags
    }

    if not notCredible:
        rfoodtruck = requests.post(postlink, headers=useragentheader, json=returnDictionary)
        if rfoodtruck.status_code == 200:
            print("Adding successful!")

            req = requests.get(urlSearchReviews, headers=headers)
            reviewsJSON = req.json()
            for review in reviewsJSON['reviews']:
                returnJSON = rfoodtruck.json()
                Name = review['user']['name']
                Comment = review['text']
                Rating = review['rating']
                Date = review['time_created']
                DateSplit = Date.split(' ')
                Date = DateSplit[0] + "T" + DateSplit[1] + "Z"
                Origin = 'Yelp'
                newReview = {
                    'reviewerName': Name,
                    'foodTruck': returnJSON['id'],
                    'comment': Comment,
                    'rating': Rating,
                    'date': Date,
                    'origin': Origin
                }
                r = requests.post(reviewURL, headers=useragentheader, json=newReview)
                if r.status_code == 200:
                    print("Review from " + Name + " added.")

        else:
            print("Could not add " + Name + " to the database.")

def putAllInDb(input, postlink):
    businessList = input['businesses']

    for b in businessList:

        putOneInDb(b, postlink)


def getYelpData(inputLink):
    url = 'https://api.yelp.com/v3/businesses/search'

    #if too many results make a radius limit and try geolocations instead of location term
    params = {'term': 'food truck', 'location': 'Austin', 'limit': 50}
    req = requests.get(url, params=params, headers=headers)
    print('The status code is {}'.format(req.status_code))
    yelpBusinesses = req.json()
    putAllInDb(yelpBusinesses, inputLink)

    params = {'term': 'food trucks', 'location': 'Austin', 'limit': 50}
    req = requests.get(url, params=params, headers=headers)
    print('The status code is {}'.format(req.status_code))
    yelpBusinesses = req.json()
    putAllInDb(yelpBusinesses, inputLink)


def parse_google_business(business, postlink):
    notCredible = False
    useragentheader = {'User-agent': 'MunchCritic/1.0'}

    Name = "ERROR: No name!"
    if 'name' in business:
        Name = business['name']

    print("Adding " + Name + " to the database...")

    id = "null"
    if 'id' in business:
        id = business['place_id']

    Address = "No address listed..."
    if 'formatted_address' in business:
        unformattedAddress = business['formatted_address'].split(',')
        if len(unformattedAddress) >= 2:
            Address = unformattedAddress[0] + '\n' + unformattedAddress[1] + ', ' + unformattedAddress[2]

    foodtruckexistsparams = {'name': Name}
    r = requests.get(postlink, foodtruckexistsparams)
    response = r.json()

    if len(response) > 0:
        for conflict in response:
            conAddress = conflict['address']
            if conAddress == Address:
                print("ERROR: Food truck already exists in database.")
                return

    phoneurl = 'https://maps.googleapis.com/maps/api/place/details/json'
    params = {'key': places_key, 'place_id': id}

    req = requests.get(phoneurl, params=params)
    #print('The status code is {}'.format(req.status_code))
    business_info = req.json()

    #todo: verify
    PhoneNumber = ''
    if 'formatted_phone_number' in business_info['result']:
        PhoneNumber = business_info['result']['formatted_phone_number']

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

    if 'opening_hours' in business_info['result']:
        if 'weekday_text' in business_info['result']['opening_hours']:
            dayIndex = 0
            for hourresult in business_info['result']['opening_hours']['weekday_text']:
                splitHours = hourresult.split(" ")
                if len(splitHours) > 2:
                    tempstart = '99:99'
                    tempend = '99:99'
                    if splitHours[2] == 'PM':
                        startArray = splitHours[1].split(':')
                        tempstart = str(int(startArray[0]) + 12) + ":" + startArray[1]
                    elif splitHours[2] == '–':
                        tempstart = '99:99'
                        tempend = '99:99'
                        if dayIndex == 0:
                            mondayStart = tempstart
                            mondayEnd = tempend
                        if dayIndex == 1:
                            tuesdayStart = tempstart
                            tuesdayEnd = tempend
                        if dayIndex == 2:
                            wednesdayStart = tempstart
                            wednesdayEnd = tempend
                        if dayIndex == 3:
                            thursdayStart = tempstart
                            thursdayEnd = tempend
                        if dayIndex == 4:
                            fridayStart = tempstart
                            fridayEnd = tempend
                        if dayIndex == 5:
                            saturdayStart = tempstart
                            saturdayEnd = tempend
                        if dayIndex == 6:
                            sundayStart = tempstart
                            sundayEnd = tempend
                        continue
                    else:
                        if splitHours[1] == '12:00':
                            tempstart = '00:00'
                        else:
                            tempstart = splitHours[1]
                            splitTempEnd = tempstart.split(':')
                            if int(splitTempEnd[0]) < 10:
                                tempstart = '0' + tempstart
                    if splitHours[5] == 'PM':
                        endArray = splitHours[4].split(':')
                        tempend = str(int(endArray[0]) + 12) + ":" + endArray[1]
                    else:
                        if splitHours[4] == '12:00':
                            tempend = '00:00'
                        else:
                            tempend = splitHours[4]
                            splitTempEnd = tempend.split(':')
                            if int(splitTempEnd[0]) < 10:
                                tempend = '0' + tempend


                    if dayIndex == 0:
                        mondayStart = tempstart
                        mondayEnd = tempend
                    if dayIndex == 1:
                        tuesdayStart = tempstart
                        tuesdayEnd = tempend
                    if dayIndex == 2:
                        wednesdayStart = tempstart
                        wednesdayEnd = tempend
                    if dayIndex == 3:
                        thursdayStart = tempstart
                        thursdayEnd = tempend
                    if dayIndex == 4:
                        fridayStart = tempstart
                        fridayEnd = tempend
                    if dayIndex == 5:
                        saturdayStart = tempstart
                        saturdayEnd = tempend
                    if dayIndex == 6:
                        sundayStart = tempstart
                        sundayEnd = tempend
                else:
                    tempstart = '99:99'
                    tempend = '99:99'
                    if dayIndex == 0:
                        mondayStart = tempstart
                        mondayEnd = tempend
                    if dayIndex == 1:
                        tuesdayStart = tempstart
                        tuesdayEnd = tempend
                    if dayIndex == 2:
                        wednesdayStart = tempstart
                        wednesdayEnd = tempend
                    if dayIndex == 3:
                        thursdayStart = tempstart
                        thursdayEnd = tempend
                    if dayIndex == 4:
                        fridayStart = tempstart
                        fridayEnd = tempend
                    if dayIndex == 5:
                        saturdayStart = tempstart
                        saturdayEnd = tempend
                    if dayIndex == 6:
                        sundayStart = tempstart
                        sundayEnd = tempend
                dayIndex += 1

    Hours = [[sundayStart, sundayEnd],
             [mondayStart, mondayEnd],
             [tuesdayStart, tuesdayEnd],
             [wednesdayStart, wednesdayEnd],
             [thursdayStart, thursdayEnd],
             [fridayStart, fridayEnd],
             [saturdayStart, saturdayEnd]]

    Photos = ["https://www.ccms.edu/wp-content/uploads/2018/07/Photo-Not-Available-Image.jpg"]

    Tags = business_info['result']['types']
    Description = ""
    Location = [business_info['result']['geometry']['location']['lat'],business_info['result']['geometry']['location']['lng']]
    Website = ''

    returnDictionary = {
        "name": Name,
        "address": Address,
        "location": Location,
        "hours": Hours,
        "photos": Photos,
        "website": Website,
        "phoneNumber": PhoneNumber,
        "description": Description,
        "tags": Tags
    }

    if not notCredible:
        r = requests.post(postlink, headers=useragentheader, json=returnDictionary)
        if r.status_code == 200:
            print("Adding successful!")

            for review in business_info['result']['reviews']:
                Name = review['author_name']
                Comment = review['text']
                Rating = review['rating']
                Date = review['time']
                tz = pytz.timezone('America/Los_Angeles')
                Date = datetime.fromtimestamp(Date, tz).isoformat()
                Origin = 'Google'
                newReview = {
                    'reviewerName': Name,
                    'foodTruck': id,
                    'comment': Comment,
                    'rating': Rating,
                    'date': Date,
                    'origin': Origin
                }
                reviewURL = postlink[:-10] + "reviews"
                r = requests.post(reviewURL, headers=useragentheader, json=newReview)
                if r.status_code == 200:
                    print("Review from " + Name + " added.")


        else:
            print("Could not add " + Name + " to the database.")





def put_all_gmap_in_db(input, postlink):
    for business in input['results']:
        parse_google_business(business, postlink)

def getPlacesData(inputLink):
    url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
    # //30.2672 -97.7431
    params = {'key': places_key, 'input': 'food trucks', 'inputtype': 'textquery', 'locationbias': 'point:30.267200,-97.743100'}
    req = requests.get(url, params=params, headers=headers)
    print('The status code is {}'.format(req.status_code))
    places_businesses = req.json()
    put_all_gmap_in_db(places_businesses, inputLink)


def printBusinesses(input):
    businessList = input['businesses']
    i = 1
    for b in businessList:
        print("\n" + str(i) + ": ")
        if 'name' in b:
            print(b['name'])
        Address = "No address listed..."
        notCredible = False
        if 'location' in b:
            address = b['location']['display_address']
            if len(address) >= 2:
                Address = address[0] + '\n' + address[1]
            else:
                notCredible = True

            if not notCredible:
                print(Address)
        i = i + 1
    return

def searchSpecificTruck(inputString, inputLink):
    url = 'https://api.yelp.com/v3/businesses/search'
    params = {'term': inputString, 'location': 'Austin', 'limit': 5}
    req = requests.get(url, params=params, headers=headers)
    print('The status code is {}'.format(req.status_code))
    yelpBusinesses = req.json()

    print("Here are the businesses we found: ")
    printBusinesses(yelpBusinesses)

    print("\nEnter the number of the food truck you want to add...\nType q to quit.\n")
    while True:
        argument = input('')
        if argument in ['q']:
            break
        elif argument in ['1','2','3','4','5']:
            putOneInDb(yelpBusinesses['businesses'][int(argument) - 1], inputLink)
        else:
            print("Invalid Argument: " + argument)
        print("\nAdd another food truck or press q to quit...")


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
            getPlacesData('http://localhost/foodtrucks')
        if command in ["3"]:
            print()
            print("What is the name of the truck you want to add?\n")
            truckName = input('')
            print("Searching for " + truckName + "...")
            searchSpecificTruck(truckName, 'http://localhost/foodtrucks')

    elif server in ["2"]:
        print("Running on heroku...")

        if command in ["1"]:
            getYelpData('http://munch-server.herokuapp.com/foodtrucks')
        if command in ["2"]:
            print("You chose: Update Google")
        if command in ["3"]:
            print()
            print("What is the name of the truck you want to add?\n")
            truckName = input('')
            print("Adding " + truckName + "...")
            searchSpecificTruck(truckName, 'http://munch-server.herokuapp.com/foodtrucks')