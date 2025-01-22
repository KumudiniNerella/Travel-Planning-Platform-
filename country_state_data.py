import pycountry
import unicodedata
from pymongo import MongoClient
import random

client = MongoClient("mongodb://localhost:27017/")
db = client.travel_recommendation_system 
country_state_collection = db.country_state_mapping
state_visit_collection = db.state_visit_mapping

def normalize_name(name):
    # Normalize Unicode characters to ASCII, ignore errors for unsupported characters
    return unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii')

def get_country_to_states():
    # Dictionary to store countries and their subdivisions (states)
    country_to_states = {}

    # Loop through all countries available in pycountry
    for country in pycountry.countries:
        country_code = country.alpha_2  # Get the ISO alpha-2 country code
        # Normalize each state's name
        states_list = [normalize_name(subdivision.name) for subdivision in pycountry.subdivisions.get(country_code=country_code)]
        
        if states_list:
            # Add country and its normalized states list to the dictionary
            country_to_states[country.name] = states_list

    return country_to_states

# Generate the dictionary
country_states_dict = get_country_to_states()

states_list = list(country_states_dict.values())
states_list = [j for i in states_list for j in i]
random_number_list = [random.randint(10,150) for i in states_list]
states_dict = dict(zip(states_list, random_number_list))

if __name__ == "__main__":
    country_state_collection.insert_one(country_states_dict)
    state_visit_collection.insert_one(states_dict)
