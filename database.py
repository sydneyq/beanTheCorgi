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
        self.db.profile.remove(toRemove)

    def countProfiles(self, findCriteria):
        return self.db.profile.count(findCriteria)

    #companion
    def insertCompanionProfile(self, toInsert):
        self.db.companion.insert(toInsert)

    def findCompanionProfile(self, findCriteria):
        return self.db.companion.find_one(findCriteria)

    def findCompanionProfiles(self, findCriteria):
        return self.db.companion.find(findCriteria)

    def updateCompanionProfile(self, updateCritera, change):
        self.db.companion.update(updateCritera, change)

    def removeCompanionProfile(self, toRemove):
        self.db.companion.remove(toRemove)

    def countCompanionProfiles(self, findCriteria):
        return self.db.companion.count(findCriteria)

    #quote
    def insertQuote(self, toInsert):
        self.db.quote.insert(toInsert)

    def findQuotes(self, findCriteria):
        return self.db.quote.find(findCriteria)

    def findQuote(self, findCriteria):
        return self.db.quote.find_one(findCriteria)

    def removeQuote(self, toRemove):
        self.db.quote.remove(toRemove)

    def countQuotes(self, findCriteria):
        return self.db.quote.count(findCriteria)

    #badges
    def findBadge(self, findCriteria):
        return self.db.badge.find_one(findCriteria)

    #meta
    def findMeta(self, findCriteria):
        return self.db.meta.find_one(findCriteria)

    def updateMeta(self, updateCritera, change):
        self.db.meta.update(updateCritera, change)

    #db
    def makeColumn(self, title, value):
        self.db.profile.update({},{"$set": {title: value}},upsert=False,multi=True)

    def renameColumn(self, old, new):
        self.db.profile.update({},{"$rename": {old: new}},upsert=False,multi=True)

    def removeColumn(self, col):
        self.db.profile.update({},{"$unset":{col: 1}},upsert=False,multi=True)
