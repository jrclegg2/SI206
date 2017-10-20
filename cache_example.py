import urllib.request, urllib.parse, urllib.error
import json

serviceurl = 'http://maps.googleapis.com/maps/api/geocode/json?'
CACHE_FNAME = 'cache_geo_locations.json' # String for your file. We want the JSON file type, bcause that way, we can easily get the information into a Python dictionary!

try:
    cache_file = open(CACHE_FNAME, 'r') # Try to read the data from the file
    cache_contents = cache_file.read()  # If it's there, get it into a string
    CACHE_DICTION = json.loads(cache_contents) # And then load it into a dictionary
    cache_file.close() # Close the file, we're good, we got the data in a dictionary.
except:
    CACHE_DICTION = {}

## Helper functions not necessary

def getLocationWithCaching(loc):
    url = serviceurl + urllib.parse.urlencode(
        {'address': loc})

    if loc in CACHE_DICTION:
        print("Data was in the cache")
        return CACHE_DICTION[loc]
    else:
        print("Making a request for new data...")
        uh = urllib.request.urlopen(url)
        data = uh.read().decode()
        try:
            CACHE_DICTION[loc] =  json.loads(data)
            dumped_json_cache = json.dumps(CACHE_DICTION)
            fw = open(CACHE_FNAME,"w")
            fw.write(dumped_json_cache)
            fw.close() # Close the open file
            return CACHE_DICTION[loc]
        except:
            print("Wasn't in cache and wasn't valid search either")
            return None


while True:
    address = input('Enter location: ')
    if len(address) < 1: break
    data = getLocationWithCaching(address)
    country = data["results"][0]["address_components"]
    for d in country:
        if 'country' in d["types"]:
            print(d["short_name"])
