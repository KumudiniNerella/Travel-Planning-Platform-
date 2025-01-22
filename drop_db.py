from pymongo import MongoClient

# Establish MongoDB connection
client = MongoClient("mongodb://localhost:27017/")

# Specify the database name
db_name = "travel_recommendation_system"

# Drop the database
client.drop_database(db_name)

print(f"Database '{db_name}' has been deleted.")
