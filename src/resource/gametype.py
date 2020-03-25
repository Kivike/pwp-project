from flask_restful import Resource, url_for
from flask import request, Response
from sqlalchemy.exc import IntegrityError
from src.utils import GametypeBuilder
from src.utils import create_error_response
from src.orm_models import GameType
from src.extensions import db
import json
from jsonschema import validate, ValidationError

MASON = "application/vnd.mason+json"
NAMESPACE_URL = "/gamescore/link-relations#"
PROFILE_URL = "/profiles/player/"

class GametypeCollection(Resource):
    def get(self):
        pass #TODO

    def post(self):
        pass #TODO

class GametypeResource(Resource):
    def get(self, gametype_name):
        pass #TODO

    def put(self, gametype_name):
        pass #TODO

    def delete(self, gametype_name):
        pass #TODO