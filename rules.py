import pymongo

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["iptables_rules"]
collection = db["rules"]

# Fetch predefined rules from MongoDB
predefined_rules = collection.find()

print("Predefines rules \n",predefined_rules)
# Convert MongoDB cursor to list of dictionaries
predefined_rules_list = list(predefined_rules)
print("Predefines rules list \n",predefined_rules_list)
# Now, `predefined_rules_list` contains the fetched predefined rules
# You can pass this list to your Flask route for rendering the template
