from setting import DB_USERNAME
from setting import DB_PASSWORD
from pymongo import MongoClient

# CONNECTION = "mongodb+srv://yoshi:<password>@cluster0.f5nmm.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"


CONNECTION = "mongodb+srv://{}:{}@cluster0.f5nmm.mongodb.net/post?retryWrites=true&w=majority".format(
    DB_USERNAME, DB_PASSWORD)


class DBWrapper:
    def __init__(self):
        self.client = MongoClient(CONNECTION)  # 括號中未給引數的話，表示連線至本地端的 MongoDB server
        self.db = self.client.face_book_crawler

    def insert_post(self, p_location, p_time, p_content, p_links):
        data = {
            "p_location": p_location,
            "p_time": p_time,
            "p_content": p_content,
            "p_links": p_links,
        }
        # self.db.post.insert_one(data)
        self.db.post.update_one({"p_links": p_links}, {"$set": {"p_time": p_time}})  # 更新臉書貼文顯示時間
        self.db.post.update_one({"p_links": p_links}, {"$set": data}, upsert=True)
