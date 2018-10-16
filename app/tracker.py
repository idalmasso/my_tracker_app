from app import mongo
from flask import current_app
from bson.objectid import ObjectId
import os
from bs4 import BeautifulSoup
import urllib.request
import json
from pathlib import Path


class Tracker(object):
    title = ''
    file_paths = ''

    def __init__(self, tracker=None):
        if tracker is not None:
            self.number = tracker.get('number', '')
            self.title = tracker.get('title', '')
            self.description = tracker.get('description', None)
            self.file_paths = tracker.get('file_paths', None)
            self.id = str(tracker.get('_id', ''))
            self.status = tracker.get('status', None)
            self.priority = tracker.get('priority', None)
            self.requires_id = int(tracker.get('requires_id', '-1'))

    def remove_tracker(self):
        mongo.db.trackers.delete_one({'_id': ObjectId(self.id)})

    @staticmethod
    def add_tracker(title):
        trk = mongo.db.trackers.find_one({'title': title})
        if trk is not None:
            return Tracker(trk)
        max_val=mongo.db.trackers.find_one({},{'number':1}, sort=[('number',-1)]).get('number',1)
        trk_id = mongo.db.trackers.insert({'title': title, 'number':max_val+1 ,'description':'', 'file_paths':[]})
        tracker = Tracker.get_tracker(str(trk_id))
        return tracker

    @staticmethod
    def get_list_trackers(page_number, tracker_per_page):
        class Object(object):
            pass

        list_tracker = Object()
        list_tracker.has_prev = (page_number > 1)
        list_tracker.prev = page_number - 1
        list_tracker.next = page_number + 1
        cont = mongo.db.trackers.count()
        list_tracker.has_next = (cont > tracker_per_page * page_number)
        skips = tracker_per_page * (page_number - 1)
        cursor = mongo.db.trackers.find().skip(skips).limit(tracker_per_page)
        list_tracker.trackers = [Tracker(tracker) for tracker in cursor]
        return list_tracker

    @staticmethod
    def get_tracker(id):
        tracker = mongo.db.trackers.find_one({'_id': ObjectId(id)})
        if not tracker:
            return None
        return Tracker(tracker)

