import json
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client.travel_recommendation_system

user_collection = db.users
destination_collection = db.destinations
booking_collection = db.bookings
country_state_collection = db.country_state_mapping
state_visit_collection = db.state_visit_mapping

def read_json(file_path):
    with open(file_path) as f:
        json_data = json.load(f)
    return json_data

def get_userdata_by_username(username):
    user_data = None
    json_data = read_json('_secret_auth_.json')
    for user in json_data:
        if user.get("username") == username:
            user_data = user.copy()
            del user_data['password']
            return user_data
    return user_data

def get_state_visit_mapping():
    d = list(state_visit_collection.find())[0]
    del d['_id']
    return d

def get_country_state_mapping():
    d = list(country_state_collection.find())[0]
    del d['_id']
    return d

def update_user_data(user_data, update = False):
    print(user_data)
    if update:
        user_collection.update_one(
                {"username": user_data["username"]},  # Filter by destinationid
                {"$set": user_data},  # Update the document with new data
                upsert=True  # Insert if it doesn't exist
            )
    else:
        user_collection.insert_one(user_data)

def get_user_document(username):
    # Search for the user document by username
    user_document = user_collection.find_one({"username": username})
    # Return the document if found, else None
    if user_document:
        del user_document['_id']
    return user_document if user_document else None

def get_all_destination_activities():
    d = list(destination_collection.find())
    activities_list = [destination['activityTags'] for destination in d]
    activities_list = [j for i in activities_list for j in i]
    return list(set(activities_list))

def recommend_destination(username, var = 'country'):
    user_data = user_collection.find_one({"username": username})
    var_value = user_data[var]
    if var == "activityTags":
        destination_data = destination_collection.find({var:{"$in": var_value}})
    else:
        destination_data = destination_collection.find({var: var_value})
    destination_data = list(destination_data)
    booking_data = list(booking_collection.find({"username": user_data['username']}))
    if booking_data:
        destinationid = [booking['destinationid'] for booking in booking_data]
        destination_data = list(filter(lambda x: x['destinationid'] not in destinationid, destination_data))
    [i.pop('_id') for i in destination_data]
    [i.pop('destinationid') for i in destination_data]
    return destination_data

def search_destination(state, season=None, activity_list=[]):
    # Build the filter dictionary based on provided parameters
    filter_query = {}

    # Add country filter if provided
    filter_query['state'] = state

    # Add season filter if provided
    if season:
        filter_query['bestSeason'] = season

    # Add activity filter if activity_list is not empty
    if activity_list:
        filter_query['activityTags'] = {"$in": activity_list}

    # Query the collection with the filter
    matching_destinations = list(destination_collection.find(filter_query))

    return matching_destinations

def search_destination_by_name(name):
    # Use regex with case-insensitive option to search for name as a substring
    name_query = {"name": {"$regex": name, "$options": "i"}}

    # Find all destinations matching the regex query
    matching_destinations = list(destination_collection.find(name_query))
    [i.pop('_id') for i in matching_destinations]
    return matching_destinations

def delete_booking(bookingid):
    booking_collection.delete_one({"bookingid": bookingid})

def insert_booking(booking_data):
    booking_collection.insert_one(booking_data)

def get_all_bookings_of_user(username):
    booking_data = booking_collection.find({"username": username})
    booking_data = list(booking_data)
    [i.pop('_id') for i in booking_data]
    return booking_data

def get_all_destination(destination_id_list):
    destination_data = []
    for destinationid in destination_id_list:
        destination_data.append(destination_collection.find_one({"destinationid": destinationid}))
    [i.pop('_id') for i in destination_data]
    return destination_data


if __name__ == "__main__":
    username = 'nakul74'
