from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client.travel_recommendation_system 
destination_collection = db.destinations

destination_data = [
    # Maharashtra
    {
        "destinationid": "maha001",
        "name": "Gateway of India",
        "imagePath": "http://example.com/gateway.jpg",
        "country": "India",
        "state": "Maharashtra",
        "oneLineDescription": "An iconic arch monument in Mumbai overlooking the Arabian Sea.",
        "bestSeason": "Winter",
        "averageCost": 500,
        "activityTags": ["historical", "architecture", "sightseeing"],
        "popularAttractions": ["Marine Drive", "Elephanta Caves"],
        "rating": 4.6,
        "historybookings" : 0
    },
    {
        "destinationid": "maha002",
        "name": "Ajanta Caves",
        "imagePath": "http://example.com/ajanta.jpg",
        "country": "India",
        "state": "Maharashtra",
        "oneLineDescription": "Ancient Buddhist rock-cut caves known for their frescoes and sculptures.",
        "bestSeason": "Winter",
        "averageCost": 800,
        "activityTags": ["historical", "caves", "UNESCO World Heritage"],
        "popularAttractions": ["Ellora Caves", "Grishneshwar Temple"],
        "rating": 4.8,
        "historybookings" : 0
    },
    # (more destinations for Maharashtra...)

    # Kerala
    {
        "destinationid": "ker001",
        "name": "Alleppey Backwaters",
        "imagePath": "http://example.com/alleppey.jpg",
        "country": "India",
        "state": "Kerala",
        "oneLineDescription": "Famous backwaters with houseboat cruises through scenic lagoons.",
        "bestSeason": "Monsoon",
        "averageCost": 2500,
        "activityTags": ["boating", "scenic", "nature"],
        "popularAttractions": ["Kumarakom", "Vembanad Lake"],
        "rating": 4.9,
        "historybookings" : 0
    },
    {
        "destinationid": "ker002",
        "name": "Munnar",
        "imagePath": "http://example.com/munnar.jpg",
        "country": "India",
        "state": "Kerala",
        "oneLineDescription": "Hill station known for its tea plantations and scenic beauty.",
        "bestSeason": "Monsoon",
        "averageCost": 2000,
        "activityTags": ["hiking", "nature", "tea plantations"],
        "popularAttractions": ["Eravikulam National Park", "Tea Museum"],
        "rating": 4.8,
        "historybookings" : 0
    },
    # (more destinations for Kerala...)

    # Rajasthan
    {
        "destinationid": "raj001",
        "name": "Jaipur - Pink City",
        "imagePath": "http://example.com/jaipur.jpg",
        "country": "India",
        "state": "Rajasthan",
        "oneLineDescription": "The capital city, famous for its forts and royal palaces.",
        "bestSeason": "Summer",
        "averageCost": 3000,
        "activityTags": ["historical", "palaces", "shopping"],
        "popularAttractions": ["Amber Fort", "City Palace", "Hawa Mahal"],
        "rating": 4.7,
        "historybookings" : 0
    },
    {
        "destinationid": "raj002",
        "name": "Udaipur",
        "imagePath": "http://example.com/udaipur.jpg",
        "country": "India",
        "state": "Rajasthan",
        "oneLineDescription": "The city of lakes, known for its beautiful palaces and romantic scenery.",
        "bestSeason": "Winter",
        "averageCost": 3500,
        "activityTags": ["lakes", "palaces", "scenic"],
        "popularAttractions": ["Lake Pichola", "City Palace", "Jagdish Temple"],
        "rating": 4.9,
        "historybookings" : 0
    },
    # (more destinations for Rajasthan...)

    # Karnataka
    {
        "destinationid": "kar001",
        "name": "Coorg",
        "imagePath": "http://example.com/coorg.jpg",
        "country": "India",
        "state": "Karnataka",
        "oneLineDescription": "A picturesque hill station known for coffee plantations and waterfalls.",
        "bestSeason": "Monsoon",
        "averageCost": 2200,
        "activityTags": ["nature", "hiking", "coffee plantations"],
        "popularAttractions": ["Abbey Falls", "Dubare Elephant Camp"],
        "rating": 4.7,
        "historybookings" : 0
    },
    {
        "destinationid": "kar002",
        "name": "Hampi",
        "imagePath": "http://example.com/hampi.jpg",
        "country": "India",
        "state": "Karnataka",
        "oneLineDescription": "A UNESCO World Heritage site with ancient ruins of temples and palaces.",
        "bestSeason": "Summer",
        "averageCost": 1500,
        "activityTags": ["historical", "UNESCO World Heritage", "ruins"],
        "popularAttractions": ["Virupaksha Temple", "Vijaya Vittala Temple"],
        "rating": 4.8,
        "historybookings" : 0
    },
    # (more destinations for Karnataka...)

    # Himachal Pradesh
    {
        "destinationid": "hp001",
        "name": "Manali",
        "imagePath": "http://example.com/manali.jpg",
        "country": "India",
        "state": "Himachal Pradesh",
        "oneLineDescription": "A scenic hill station known for adventure sports and natural beauty.",
        "bestSeason": "Summer",
        "averageCost": 1800,
        "activityTags": ["trekking", "skiing", "nature"],
        "popularAttractions": ["Rohtang Pass", "Solang Valley"],
        "rating": 4.8,
        "historybookings" : 0
    },
    {
        "destinationid": "hp002",
        "name": "Shimla",
        "imagePath": "http://example.com/shimla.jpg",
        "country": "India",
        "state": "Himachal Pradesh",
        "oneLineDescription": "A charming hill station, famous for its colonial architecture and Mall Road.",
        "bestSeason": "Winter",
        "averageCost": 1600,
        "activityTags": ["nature", "colonial architecture", "shopping"],
        "popularAttractions": ["Mall Road", "Jakhoo Temple"],
        "rating": 4.7,
        "historybookings" : 0
    },
    # (more destinations for Himachal Pradesh...)
]

if __name__ == "__main__":
    for destination in destination_data:
        destination_collection.update_one(
            {"destinationid": destination["destinationid"]},  # Filter by destinationid
            {"$set": destination},  # Update the document with new data
            upsert=True  # Insert if it doesn't exist
        )
