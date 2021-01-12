from flask_testing import TestCase

from pp_project import engine, Session
from pp_project.models import Base


class TestBase(TestCase):
    def create_app(self):
        from pp_project import app
        return app

    def setUp(self):
        self.app = self.create_app().test_client()
        self.connection = engine.connect()
        self.session = Session(bind=self.connection)
        Base.metadata.create_all(engine)

    def tearDown(self):
        Base.metadata.drop_all(engine)
        self.session.close()
        self.connection.close()

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
