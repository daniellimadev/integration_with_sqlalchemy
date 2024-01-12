from pymongo import MongoClient

connection_string = "mongodb://admin:password@localhost:27017/?authSource=admin"
client = MongoClient(connection_string)
db_connection = client["myBank"]

print(db_connection)
print()
collection = db_connection.get_collection("myCollection")

print(collection)
print()

search_filter = { "I am": "here" }
response = collection.find(search_filter)

for registry in response: print(registry)

collection.insert_one({
    "I am": "Inserting",
    "Numbers": [123, 456, 789]
})