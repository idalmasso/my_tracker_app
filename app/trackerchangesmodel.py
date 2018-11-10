from app import mongo
from bson.objectid import ObjectId
import datetime


class TrkChanges(object):
    username = ''
    tracker_id = ''
    tracker_identifier = ''
    datetime = ''
    project = ''
    action = ''

    def __init__(self, change=None):
        if change is not None:
            self.username = change.get('username', '')
            self.tracker_id = change.get('tracker_id', '')
            self.tracker_identifier = change.get('tracker_identifier', '')
            self.datetime = change.get('datetime', '')
            self.project = change.get('project', '')
            self.id = str(change.get('_id', ''))
            self.action = change.get('action', '')

    @staticmethod
    def create_change(username,tracker,project,action):
        chg_id = mongo.db.changes.insert({'username': username,
                                          'tracker_id': str(tracker.id),
                                          'tracker_identifier': (tracker.prefix+'-'+"%04d" % tracker.number),
                                          'project': project,
                                          'datetime': datetime.datetime.utcnow(),
                                          'action': action})
        chg = TrkChanges.get_change(str(chg_id))
        return project

    @staticmethod
    def get_list_changes(page_number, changes_per_page, filtering):
        class Object(object):
            pass

        list_changes = Object()
        list_changes.has_prev = (page_number > 1)
        list_changes.prev = page_number - 1
        list_changes.next = page_number + 1
        cont = mongo.db.changes.count(filtering)
        list_changes.has_next = (cont > changes_per_page * page_number)
        skips = changes_per_page * (page_number - 1)
        cursor = mongo.db.changes.find(filtering).sort('datetime', -1).skip(skips).limit(changes_per_page)
        list_changes.changes = [TrkChanges(change) for change in cursor]
        return list_changes

    @staticmethod
    def get_change(id):
        chg = mongo.db.list_changes.find_one({'_id': ObjectId(id)})
        if not chg:
            return None
        return TrkChanges(chg)
