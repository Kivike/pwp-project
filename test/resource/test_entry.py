import unittest
from sqlalchemy import exc
from sqlalchemy import orm

from src.app import create_app, db

import json

class TestEntry(unittest.TestCase):

    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def testEntrypoint(self):
        '''
        Test for success response status
        '''
        url = "/api/"
        response = self.client.get(url)
        assert response.status_code == 200