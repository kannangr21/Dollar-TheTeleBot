def get_database():
    from pymongo import MongoClient
    import pymongo
    import urllib
    from decouple import config
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    client = pymongo.MongoClient(f"mongodb+srv://{config('USER_NAME')}:"+urllib.parse.quote(config('PASSWORD'))+f"@{config('user')}.bympf.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client['test']
# This is added so that many files can reuse the function get_database()
    return db
   
   
   
   
   
   
    '''dbname = get_database()
collection = dbname['userevents']
item_1 = {
"_id" : "01",
"user_name" : "Kannan",
"event" : "Chennai",
"expense" : 5000,
"date" : "12/10/2021"
}
collection.insert(item_1)
'''