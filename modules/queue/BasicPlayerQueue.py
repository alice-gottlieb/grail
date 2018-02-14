"""Queue item for basic analysis by irwin"""
from collections import namedtuple
from datetime import datetime
import pymongo

BasicPlayerQueue = namedtuple('BasicPlayerQueue', ['id', 'origin'])

class BasicPlayerQueueBSONHandler:
    @staticmethod
    def reads(bson):
        return BasicPlayerQueue(
            id=bson['_id'],
            origin=bson['origin'])

    @staticmethod
    def writes(basicPlayerQueue):
        return {
            '_id': basicPlayerQueue.id,
            'origin': basicPlayerQueue.origin,
            'date': datetime.now()
        }

class BasicPlayerQueueDB(namedtuple('BasicPlayerQueueDB', ['basicPlayerQueueColl'])):
    def write(self, basicPlayerQueue):
        self.basicPlayerQueueColl.update_one(
            {'_id': basicPlayerQueue.id}, 
            {'$set': BasicPlayerQueueBSONHandler.writes(basicPlayerQueue)},
            upsert=True)

    def removeUserId(self, userId):
        self.basicPlayerQueueColl.remove({'_id': userId})

    def nextUnprocessed(self):
        basicPlayerQueueBSON = self.basicPlayerQueueColl.find_one_and_delete(
            filter={},
            sort=[("date", pymongo.ASCENDING)])
        return None if basicPlayerQueueBSON is None else BasicPlayerQueueBSONHandler.reads(basicPlayerQueueBSON)