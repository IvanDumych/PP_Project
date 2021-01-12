import base64
import unittest

from flask_testing import TestCase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pp_project.models import Base, User, Audience, Reservation
from pp_project.schemas import UserSchema
from pp_project import app
from pp_project import engine, Session


class TestUser(TestCase):
    def create_app(self):
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

    def get_test_user_data(self,
                           first_name='test_first_name',
                           second_name='test_second_name',
                           user_name='test_username',
                           password='test_password'):
        user = {
            'first_name': first_name,
            'second_name': second_name,
            'user_name': user_name,
            'password': password
        }
        return user

    def create_user(self, data=None):
        if data is None:
            data = self.get_test_user_data()
        user = User(**data)
        user.hash_password()
        self.session.add(user)
        self.session.commit()
        return user, data

    def delete_user(self, user=None):
        if user is None:
            user = self.get_test_user_data()
        self.session.query(User).delete(user)

    def test_post_user_successful(self):
        user = self.get_test_user_data()

        response = self.app.post('/user/', json=user)
        self.assertEqual(200, response.status_code)

    def test_post_user_invalid_input_405(self):
        user = self.get_test_user_data()
        user['error'] = 'error'
        response = self.app.post('/user/', json=user)
        self.assertEqual(405, response.status_code)

    def test_get_user_successful(self):
        user = self.create_user()[1]
        auth_data = f"{user['user_name']}:{user['password']}".encode()
        credentials = base64.b64encode(auth_data).decode('utf-8')
        response = self.app.get('/user/1/', headers={
            'Authorization': f'Basic {credentials}'})
        self.assertEqual(200, response.status_code)

    def test_put_user_successful(self):
        user = self.create_user()[1]
        auth_data = f"{user['user_name']}:{user['password']}".encode()
        credentials = base64.b64encode(auth_data).decode('utf-8')
        data = self.get_test_user_data()
        response = self.app.put('/user/1/', json=data, headers={
            'Authorization': f'Basic {credentials}'})
        self.assertEqual(200, response.status_code)

    def test_put_user_auth_error_username(self):
        user = self.create_user()[1]
        auth_data = f"qw:{user['password']}".encode()
        credentials = base64.b64encode(auth_data).decode('utf-8')
        response = self.app.put('/user/1/', json={'user_name': 'changed_name'}, headers={
            'Authorization': f'Basic {credentials}'})
        self.assertEqual(403, response.status_code)

    def test_put_user_error(self):
        user = self.create_user()[1]
        auth_data = f"{user['user_name']}:{user['password']}".encode()
        credentials = base64.b64encode(auth_data).decode('utf-8')
        response = self.app.put('/user/2/', json={'user_name': 'changed_name'}, headers={
            'Authorization': f'Basic {credentials}'})
        self.assertEqual(403, response.status_code)

    def test_delete_user_successful(self):
        user = self.create_user()[1]
        auth_data = f"{user['user_name']}:{user['password']}".encode()
        credentials = base64.b64encode(auth_data).decode('utf-8')
        response = self.app.delete('/user/1/', headers={
            'Authorization': f'Basic {credentials}'})
        self.assertEqual(200, response.status_code)

    def test_delete_user_not_found(self):
        user = self.create_user()[1]
        auth_data = f"{user['user_name']}:{user['password']}".encode()
        credentials = base64.b64encode(auth_data).decode('utf-8')
        response = self.app.delete('/user/2/', headers={
            'Authorization': f'Basic {credentials}'})
        self.assertEqual(403, response.status_code)

    def get_test_audience_data(self,
                               location='Lviv',
                               size=22,
                               capacity=25):
        audience = {
            'location': location,
            'size': size,
            'capacity': capacity
        }
        return audience

    def create_audience(self, data=None):
        if data is None:
            data = self.get_test_audience_data()
        audience = Audience(**data)
        self.session.add(audience)
        self.session.commit()
        return audience, data

    def test_post_audience_successful(self):
        user = self.create_user()[1]
        auth_data = f"{user['user_name']}:{user['password']}".encode()
        credentials = base64.b64encode(auth_data).decode('utf-8')
        audience = self.get_test_audience_data()
        response = self.app.post('/audience/', json=audience, headers={
            'Authorization': f'Basic {credentials}'})
        self.assertEqual(200, response.status_code)

    def test_post_audience_invalid_input_first(self):
        user = self.create_user()[1]
        auth_data = f"{user['user_name']}:{user['password']}".encode()
        credentials = base64.b64encode(auth_data).decode('utf-8')
        audience = self.get_test_audience_data()
        audience['error'] = 'error'
        response = self.app.post('/audience/', json=audience, headers={
            'Authorization': f'Basic {credentials}'})
        self.assertEqual(405, response.status_code)

    def test_post_audience_invalid_input_second(self):
        user = self.create_user()[1]
        auth_data = f"{user['user_name']}:{user['password']}".encode()
        credentials = base64.b64encode(auth_data).decode('utf-8')
        audience = self.get_test_audience_data()
        audience['size'] = -1
        response = self.app.post('/audience/', json=audience, headers={
            'Authorization': f'Basic {credentials}'})
        self.assertEqual(405, response.status_code)

    def test_get_audience_successful(self):
        user = self.create_user()[1]
        auth_data = f"{user['user_name']}:{user['password']}".encode()
        credentials = base64.b64encode(auth_data).decode('utf-8')
        self.create_audience()
        response = self.app.get('/audience/1/', headers={
            'Authorization': f'Basic {credentials}'})
        self.assertEqual(200, response.status_code)

    def test_get_audience_not_found(self):
        user = self.create_user()[1]
        auth_data = f"{user['user_name']}:{user['password']}".encode()
        credentials = base64.b64encode(auth_data).decode('utf-8')
        self.create_audience()
        response = self.app.get('/audience/2/', headers={
            'Authorization': f'Basic {credentials}'})
        self.assertEqual(403, response.status_code)

    def test_get_audiences_successful(self):
        user = self.create_user()[1]
        auth_data = f"{user['user_name']}:{user['password']}".encode()
        credentials = base64.b64encode(auth_data).decode('utf-8')
        self.create_audience()
        response = self.app.get('/audience/', headers={
            'Authorization': f'Basic {credentials}'})
        self.assertEqual(200, response.status_code)

    def test_get_audiences_not_found(self):
        user = self.create_user()[1]
        auth_data = f"{user['user_name']}:{user['password']}".encode()
        credentials = base64.b64encode(auth_data).decode('utf-8')
        response = self.app.get('/audience/', headers={
            'Authorization': f'Basic {credentials}'})
        self.assertEqual(403, response.status_code)

    def get_test_reservation_data(self,
                                  from_date='2000-01-01',
                                  to_date='2000-01-21',
                                  user_id=1,
                                  audience_id=1):
        reservation = {
            'from_date': from_date,
            'to_date': to_date,
            'user_id': user_id,
            'audience_id': audience_id
        }
        return reservation

    def create_reservation(self, data=None):
        import datetime
        if data is None:
            data = self.get_test_reservation_data()
            data['from_date'] = datetime.date(2000, 1, 1)
            data['to_date'] = datetime.date(2000, 1, 21)
        else:
            from_date = [int(i) for i in data['from_date'].split('-')]
            to_date = [int(i) for i in data['to_date'].split('-')]
            data['from_date'] = datetime.date(from_date[0], from_date[1], from_date[2])
            data['to_date'] = datetime.date(to_date[0], to_date[1], to_date[2])
        reservation = Reservation(**data)
        self.session.add(reservation)
        self.session.commit()
        return reservation, data

    def test_get_reservation_successful(self):
        self.create_user()
        self.create_audience()
        self.create_reservation()
        response = self.app.get('/reservation/')
        self.assertEqual(200, response.status_code)

    def test_post_reservation_successful(self):
        user = self.create_user()[1]
        auth_data = f"{user['user_name']}:{user['password']}".encode()
        credentials = base64.b64encode(auth_data).decode('utf-8')
        self.create_audience()
        reservation = self.get_test_reservation_data()
        response = self.app.post('/reservation/', json=reservation, headers={
            'Authorization': f'Basic {credentials}'})
        self.assertEqual(200, response.status_code)

    def test_post_reservation_invalid_input(self):
        user = self.create_user()[1]
        auth_data = f"{user['user_name']}:{user['password']}".encode()
        credentials = base64.b64encode(auth_data).decode('utf-8')
        self.create_audience()
        reservation = self.get_test_reservation_data()
        reservation['to_date'], reservation['from_date'] \
            = reservation['from_date'], reservation['to_date']
        response = self.app.post('/reservation/', json=reservation, headers={
            'Authorization': f'Basic {credentials}'})
        self.assertEqual(405, response.status_code)

    def test_post_reservation_error_date_check_from(self):
        user = self.create_user()[1]
        auth_data = f"{user['user_name']}:{user['password']}".encode()
        credentials = base64.b64encode(auth_data).decode('utf-8')
        self.create_audience()
        self.create_reservation()
        reservation = self.get_test_reservation_data()
        response = self.app.post('/reservation/', json=reservation, headers={
            'Authorization': f'Basic {credentials}'})
        self.assertEqual(405, response.status_code)

    def test_post_reservation_error_date_check_to(self):
        user = self.create_user()[1]
        auth_data = f"{user['user_name']}:{user['password']}".encode()
        credentials = base64.b64encode(auth_data).decode('utf-8')
        self.create_audience()
        data = self.get_test_reservation_data(from_date='2000-01-15')
        self.create_reservation(data=data)
        reservation = self.get_test_reservation_data()
        response = self.app.post('/reservation/', json=reservation, headers={
            'Authorization': f'Basic {credentials}'})
        self.assertEqual(405, response.status_code)

    def test_post_reservation_user_not_found(self):
        user = self.create_user()[1]
        auth_data = f"{user['user_name']}:{user['password']}".encode()
        credentials = base64.b64encode(auth_data).decode('utf-8')
        self.create_audience()
        reservation = self.get_test_reservation_data()
        reservation['user_id'] = 2
        response = self.app.post('/reservation/', json=reservation, headers={
            'Authorization': f'Basic {credentials}'})
        self.assertEqual(403, response.status_code)

    def test_post_reservation_audience_not_found(self):
        user = self.create_user()[1]
        auth_data = f"{user['user_name']}:{user['password']}".encode()
        credentials = base64.b64encode(auth_data).decode('utf-8')
        self.create_audience()
        reservation = self.get_test_reservation_data()
        reservation['audience_id'] = 2
        response = self.app.post('/reservation/', json=reservation, headers={
            'Authorization': f'Basic {credentials}'})
        self.assertEqual(403, response.status_code)

    def test_put_reservation_successful(self):
        user = self.create_user()[1]
        auth_data = f"{user['user_name']}:{user['password']}".encode()
        credentials = base64.b64encode(auth_data).decode('utf-8')
        self.create_audience()
        self.create_audience()
        self.create_reservation()
        reservation = self.get_test_reservation_data(
            # from_date='2000-01-02',
            # to_date='2000-01-22',
            # audience_id=2
        )
        reservation.pop('user_id')
        response = self.app.put('/reservation/1/', json=reservation, headers={
            'Authorization': f'Basic {credentials}'})
        self.assertEqual(200, response.status_code)

    def test_put_reservation_not_found(self):
        user = self.create_user()[1]
        auth_data = f"{user['user_name']}:{user['password']}".encode()
        credentials = base64.b64encode(auth_data).decode('utf-8')
        self.create_audience()
        self.create_audience()
        self.create_reservation()
        reservation = self.get_test_reservation_data()
        response = self.app.put('/reservation/2/', json=reservation, headers={
            'Authorization': f'Basic {credentials}'})
        self.assertEqual(403, response.status_code)

    def test_delete_reservation_successful(self):
        user = self.create_user()[1]
        auth_data = f"{user['user_name']}:{user['password']}".encode()
        credentials = base64.b64encode(auth_data).decode('utf-8')
        self.create_audience()
        self.create_reservation()
        response = self.app.delete('/reservation/1/', headers={
            'Authorization': f'Basic {credentials}'})
        self.assertEqual(200, response.status_code)

    def test_delete_user_successful_reservations(self):
        user = self.create_user()[1]
        auth_data = f"{user['user_name']}:{user['password']}".encode()
        credentials = base64.b64encode(auth_data).decode('utf-8')
        self.create_reservation()
        response = self.app.delete('/user/1/', headers={
            'Authorization': f'Basic {credentials}'})
        self.assertEqual(200, response.status_code)

    def test_delete_reservation_not_found(self):
        user = self.create_user()[1]
        auth_data = f"{user['user_name']}:{user['password']}".encode()
        credentials = base64.b64encode(auth_data).decode('utf-8')
        self.create_audience()
        response = self.app.delete('/reservation/1/', headers={
            'Authorization': f'Basic {credentials}'})
        self.assertEqual(403, response.status_code)


if __name__ == '__main__':
    unittest.main()
