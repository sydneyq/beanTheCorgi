import pymongo
import secret

class Database:

    def __init__(self):
        self.dbclient = pymongo.MongoClient(secret.DB_KEY)
        self.db = self.dbclient.bot

    def openDatabase(self):
        self.dbclient = pymongo.MongoClient(secret.DB_KEY)
        self.db = self.dbclient.bot

    def closeDatabase(self):
        self.dbclient.close()

    #profile
    def insertProfile(self, toInsert):
        self.db.profile.insert(toInsert)

    def findProfile(self, findCriteria):
        return self.db.profile.find_one(findCriteria)

    def findProfiles(self, findCriteria):
        return self.db.profile.find(findCriteria)

    def updateProfile(self, updateCritera, change):
        self.db.profile.update(updateCritera, change)

    def removeProfile(self, toRemove):
        profile = findProfile({"id": id})
        if profile is not None:
            self.db.profile.remove(toRemove)

    def count(self, findCriteria):
        return self.db.profile.count(findCriteria)
