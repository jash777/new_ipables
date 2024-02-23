import pymongo
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['agents_manager']
collection = db['agnets']

# Define 20 iptables rules
# rules = [
#     {'id': 1, 'protocol': 'udp', 'destination_port': 53, 'action': 'ACCEPT', 'description': 'Allow DNS lookups'},
#     {'id': 2, 'protocol': 'tcp', 'destination_port': 80, 'action': 'ACCEPT', 'description': 'Allow HTTP traffic'},
#     {'id': 3, 'protocol': 'tcp', 'destination_port': 443, 'action': 'ACCEPT', 'description': 'Allow HTTPS traffic'},
#     {'id': 4, 'protocol': 'tcp', 'destination_port': 22, 'action': 'ACCEPT', 'description': 'Allow SSH traffic'},
#     {'id': 5, 'protocol': 'udp', 'destination_port': 123, 'action': 'ACCEPT', 'description': 'Allow NTP traffic'},
#     {'id': 6, 'protocol': 'tcp', 'destination_port': 25, 'action': 'ACCEPT', 'description': 'Allow SMTP traffic'},
#     {'id': 7, 'protocol': 'tcp', 'destination_port': 110, 'action': 'ACCEPT', 'description': 'Allow POP3 traffic'},
#     {'id': 8, 'protocol': 'tcp', 'destination_port': 143, 'action': 'ACCEPT', 'description': 'Allow IMAP traffic'},
#     {'id': 9, 'protocol': 'udp', 'destination_port': 161, 'action': 'ACCEPT', 'description': 'Allow SNMP traffic'},
#     {'id': 10, 'protocol': 'tcp', 'destination_port': 389, 'action': 'ACCEPT', 'description': 'Allow LDAP traffic'},
#     {'id': 11, 'protocol': 'udp', 'destination_port': 514, 'action': 'ACCEPT', 'description': 'Allow Syslog traffic'},
#     {'id': 12, 'protocol': 'tcp', 'destination_port': 1433, 'action': 'ACCEPT', 'description': 'Allow MSSQL traffic'},
#     {'id': 13, 'protocol': 'tcp', 'destination_port': 3306, 'action': 'ACCEPT', 'description': 'Allow MySQL traffic'},
#     {'id': 14, 'protocol': 'tcp', 'destination_port': 5432, 'action': 'ACCEPT', 'description': 'Allow PostgreSQL traffic'},
#     {'id': 15, 'protocol': 'tcp', 'destination_port': 27017, 'action': 'ACCEPT', 'description': 'Allow MongoDB traffic'},
#     {'id': 16, 'protocol': 'tcp', 'destination_port': 3389, 'action': 'ACCEPT', 'description': 'Allow RDP traffic'},
#     {'id': 17, 'protocol': 'tcp', 'destination_port': 5900, 'action': 'ACCEPT', 'description': 'Allow VNC traffic'},
#     {'id': 18, 'protocol': 'tcp', 'destination_port': 3306, 'action': 'ACCEPT', 'description': 'Allow MySQL traffic'},
#     {'id': 19, 'protocol': 'tcp', 'destination_port': 389, 'action': 'ACCEPT', 'description': 'Allow LDAP traffic'},
#     {'id': 20, 'protocol': 'tcp', 'destination_port': 5432, 'action': 'ACCEPT', 'description': 'Allow PostgreSQL traffic'}
# ]


server_details = [
    {'ip': '192.168.1.10', 'port': 5050, 'id': 1},
    {'ip': '192.168.1.15', 'port': 5070, 'id': 2},
    {'ip': '192.168.1.20', 'port': 5090, 'id': 3},
    # Add more server details as needed
]
# Insert rules into MongoDB
result = collection.insert_many(server_details)
print(f"Inserted {len(result.inserted_ids)} agents")

# Query rules from MongoDB
queried_rules = collection.find()
for rule in queried_rules:
    print(rule)
