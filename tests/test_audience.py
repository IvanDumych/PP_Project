# import base64
# import unittest
#
# from flask_testing import TestCase
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
#
# from pp_project.models import Base, Audience
# from pp_project.schemas import AudienceSchema
# from pp_project import app
# from pp_project import engine, Session
#
#
# class TestAudience(TestCase):
#     def create_app(self):
#         return app
#
#     def setUp(self):
#         self.app = self.create_app().test_client()
#         self.connection = engine.connect()
#         self.session = Session(bind=self.connection)
#         Base.metadata.create_all(engine)
#
#     def tearDown(self):
#         Base.metadata.drop_all(engine)
#         self.session.close()
#         self.connection.close()
#
#     def get_test_audience_data(self,
#                                location='Lviv',
#                                size=22,
#                                capacity=25):
#         audience = {
#             'location': location,
#             'size': size,
#             'capacity': capacity
#         }
#         return audience
#
#     def create_audience(self, data=None):
#         if data is None:
#             data = self.get_test_audience_data()
#         audience = Audience(**data)
#         self.session.add(audience)
#         self.session.commit()
#         return audience, data
#
#     def delete_audience(self, audience=None):
#         if audience is None:
#             audience = self.get_test_audience_data()
#         self.session.query(audience).delete(audience)
#
#     def test_post_audience_successful(self):
#         audience = self.get_test_audience_data()
#         print(audience)
#         response = self.app.post('/audience/', json=audience)
#         self.assertEqual(200, response.status_code)
#
#     # def test_post_audience_invalid_input_405(self):
#     #     audience = self.get_test_audience_data()
#     #     audience['error'] = 'error'
#     #     response = self.app.post('/audience/', json=audience)
#     #     self.assertEqual(405, response.status_code)
#     #
#     # def test_get_audience_successful(self):
#     #     audience = self.create_audience()[1]
#     #     auth_data = f"{audience['audience_name']}:{audience['password']}".encode()
#     #     credentials = base64.b64encode(auth_data).decode('utf-8')
#     #     response = self.app.get('/audience/1/', headers={
#     #         'Authorization': f'Basic {credentials}'})
#     #     self.assertEqual(200, response.status_code)
#     #
#     # def test_put_audience_successful(self):
#     #     audience = self.create_audience()[1]
#     #     auth_data = f"{audience['audience_name']}:{audience['password']}".encode()
#     #     credentials = base64.b64encode(auth_data).decode('utf-8')
#     #     response = self.app.put('/audience/1/', json={'audience_name': 'changed_name'}, headers={
#     #         'Authorization': f'Basic {credentials}'})
#     #     self.assertEqual(200, response.status_code)
#     #
#     # def test_delete_audience_successful(self):
#     #     audience = self.create_audience()[1]
#     #     auth_data = f"{audience['audience_name']}:{audience['password']}".encode()
#     #     credentials = base64.b64encode(auth_data).decode('utf-8')
#     #     response = self.app.delete('/audience/1/', headers={
#     #         'Authorization': f'Basic {credentials}'})
#     #     self.assertEqual(200, response.status_code)
#
#
# if __name__ == '__main__':
#     unittest.main()
