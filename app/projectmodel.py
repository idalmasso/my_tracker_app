from app import mongo
from bson.objectid import ObjectId

class TrkProject(object):
    name = ''
    description = ''
    def __init__(self, prj=None):
        if prj is not None:
           self.name = prj.get('name','')
           self.description = prj.get('description','')
           self.id = str(prj.get('_id',''))

    def update_project(self):
        mongo.db.projects.update_one({'_id':ObjectId(self.id)},
                                     {'$set':{
                                         'name':self.name,
                                         'description':self.description
                                         }})

    @staticmethod
    def create_project(name,description):
        prj = mongo.db.projects.find_one({'name':name})
        if prj is not None:
            return TrkProject(prj)
        prj_id = mongo.db.projects.insert({'name': name,
                                           'description':description})
        return prj_id

    @staticmethod
    def get_list_projects(page_number, projects_per_page):
        class Object(object):
            pass

        list_project = Object()
        list_project.has_prev = (page_number > 1)
        list_project.prev = page_number - 1
        list_project.next = page_number + 1
        cont = mongo.db.projects.count()
        list_project.has_next = (cont > projects_per_page * page_number)
        skips = projects_per_page * (page_number - 1)
        cursor = mongo.db.projects.find().skip(skips).limit(projects_per_page)
        list_project.projects = [TrkProject(project) for project in cursor]
        return list_project

    @staticmethod
    def get_project(id):
        project = mongo.db.projects.find_one({'_id': ObjectId(id)})
        if not project:
            return None
        return TrkProject(project)

    @staticmethod
    def find_first():
        project = mongo.db.projects.find_one()
        if not project:
            return None
        return TrkProject(project)
