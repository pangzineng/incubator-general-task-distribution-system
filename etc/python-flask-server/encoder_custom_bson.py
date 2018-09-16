from connexion.apps.flask_app import FlaskJSONEncoder
import six

from swagger_server.models.base_model_ import Model
from bson import ObjectId, json_util
import json
from pymongo.results import InsertOneResult, UpdateResult, DeleteResult


class JSONEncoder(FlaskJSONEncoder):
    include_nulls = False

    def default(self, o):
        if isinstance(o, Model):
            dikt = {}
            for attr, _ in six.iteritems(o.swagger_types):
                value = getattr(o, attr)
                if value is None and not self.include_nulls:
                    continue
                attr = o.attribute_map[attr]
                dikt[attr] = value
            return dikt
        elif isinstance(o, ObjectId):
            return str(o)
        elif isinstance(o, InsertOneResult) or isinstance(o, UpdateResult) or isinstance(o, DeleteResult):
            return json.loads(json_util.dumps(o))
        return FlaskJSONEncoder.default(self, o)
