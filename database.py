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
