import base64
import unittest

from tests.test_base import TestBase
from tests.utils import (
    create_user, get_test_user_data,
    create_audience, get_test_audience_data,
    create_reservation, get_test_reservation_data
)


class TestReservation(TestBase):
    def test_get_reservation_successful(self):
        create_user(self.session)
        create_audience(self.session)
        create_reservation(self.session)
        response = self.app.get('/reservation/')
        self.assertEqual(200, response.status_code)

    def test_post_reservation_successful(self):
        user = create_user(self.session)[1]
        auth_data = f"{user['user_name']}:{user['password']}".encode()
        credentials = base64.b64encode(auth_data).decode('utf-8')
        create_audience(self.session)
        reservation = get_test_reservation_data()
        response = self.app.post('/reservation/', json=reservation, headers={
            'Authorization': f'Basic {credentials}'})
        self.assertEqual(200, response.status_code)

    def test_post_reservation_invalid_input(self):
        user = create_user(self.session)[1]
        auth_data = f"{user['user_name']}:{user['password']}".encode()
        credentials = base64.b64encode(auth_data).decode('utf-8')
        create_audience(self.session)
        reservation = get_test_reservation_data()
        reservation['to_date'], reservation['from_date'] \
            = reservation['from_date'], reservation['to_date']
        response = self.app.post('/reservation/', json=reservation, headers={
            'Authorization': f'Basic {credentials}'})
        self.assertEqual(405, response.status_code)

    def test_post_reservation_error_date_check_from(self):
        user = create_user(self.session)[1]
        auth_data = f"{user['user_name']}:{user['password']}".encode()
        credentials = base64.b64encode(auth_data).decode('utf-8')
        create_audience(self.session)
        create_reservation(self.session)
        reservation = get_test_reservation_data()
        response = self.app.post('/reservation/', json=reservation, headers={
            'Authorization': f'Basic {credentials}'})
        self.assertEqual(405, response.status_code)

    def test_post_reservation_error_date_check_to(self):
        user = create_user(self.session)[1]
        auth_data = f"{user['user_name']}:{user['password']}".encode()
        credentials = base64.b64encode(auth_data).decode('utf-8')
        create_audience(self.session)
        data = get_test_reservation_data(from_date='2000-01-15')
        create_reservation(self.session, data=data)
        reservation = get_test_reservation_data()
        response = self.app.post('/reservation/', json=reservation, headers={
            'Authorization': f'Basic {credentials}'})
        self.assertEqual(405, response.status_code)

    def test_post_reservation_user_not_found(self):
        user = create_user(self.session)[1]
        auth_data = f"{user['user_name']}:{user['password']}".encode()
        credentials = base64.b64encode(auth_data).decode('utf-8')
        create_audience(self.session)
        reservation = get_test_reservation_data()
        reservation['user_id'] = 2
        response = self.app.post('/reservation/', json=reservation, headers={
            'Authorization': f'Basic {credentials}'})
        self.assertEqual(403, response.status_code)

    def test_post_reservation_audience_not_found(self):
        user = create_user(self.session)[1]
        auth_data = f"{user['user_name']}:{user['password']}".encode()
        credentials = base64.b64encode(auth_data).decode('utf-8')
        create_audience(self.session)
        reservation = get_test_reservation_data()
        reservation['audience_id'] = 2
        response = self.app.post('/reservation/', json=reservation, headers={
            'Authorization': f'Basic {credentials}'})
        self.assertEqual(403, response.status_code)

    def test_put_reservation_successful(self):
        user = create_user(self.session)[1]
        auth_data = f"{user['user_name']}:{user['password']}".encode()
        credentials = base64.b64encode(auth_data).decode('utf-8')
        create_audience(self.session)
        create_audience(self.session)
        create_reservation(self.session)
        reservation = get_test_reservation_data()
        reservation.pop('user_id')
        response = self.app.put('/reservation/1/', json=reservation, headers={
            'Authorization': f'Basic {credentials}'})
        self.assertEqual(200, response.status_code)

    def test_put_reservation_not_found(self):
        user = create_user(self.session)[1]
        auth_data = f"{user['user_name']}:{user['password']}".encode()
        credentials = base64.b64encode(auth_data).decode('utf-8')
        create_audience(self.session)
        create_audience(self.session)
        create_reservation(self.session)
        reservation = get_test_reservation_data()
        response = self.app.put('/reservation/2/', json=reservation, headers={
            'Authorization': f'Basic {credentials}'})
        self.assertEqual(403, response.status_code)

    def test_delete_reservation_successful(self):
        user = create_user(self.session)[1]
        auth_data = f"{user['user_name']}:{user['password']}".encode()
        credentials = base64.b64encode(auth_data).decode('utf-8')
        create_audience(self.session)
        create_reservation(self.session)
        response = self.app.delete('/reservation/1/', headers={
            'Authorization': f'Basic {credentials}'})
        self.assertEqual(200, response.status_code)

    def test_delete_reservation_not_found(self):
        user = create_user(self.session)[1]
        auth_data = f"{user['user_name']}:{user['password']}".encode()
        credentials = base64.b64encode(auth_data).decode('utf-8')
        create_audience(self.session)
        response = self.app.delete('/reservation/1/', headers={
            'Authorization': f'Basic {credentials}'})
        self.assertEqual(403, response.status_code)
