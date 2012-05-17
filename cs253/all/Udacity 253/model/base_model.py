import datetime

__author__ = 'dhensche'

import json
from google.appengine.ext import db

class JsonModel(db.Model):
    def to_json(self):
        return json.dumps(self.to_json_serializable(), cls=ModelEncoder)
    def to_json_serializable(self):
        data = {}
        for prop in self.properties().values():
            data[prop.name] = prop.get_value_for_datastore(self)
        return data

class ModelEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        if isinstance(o, JsonModel):
            return o.to_json_serializable()
        return json.JSONEncoder.default(self, o)