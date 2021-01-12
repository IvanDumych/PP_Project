import base64
import unittest

from tests.test_base import TestBase
from tests.utils import (
    create_user, get_test_user_data,
    create_audience, get_test_audience_data,
    create_reservation, get_test_reservation_data)


class TestUser(TestBase):
    def test_post_user_successful(self):
        user = get_test_user_data()
        response = self.app.post('/user/', json=user)
        self.assertEqual(200, response.status_code)

    def test_post_user_invalid_input_405(self):
        user = get_test_user_data()
        user['error'] = 'error'
        response = self.app.post('/user/', json=user)
        self.assertEqual(405, response.status_code)

    def test_get_user_successful(self):
        user = create_user(self.session)[1]
        auth_data = f"{user['user_name']}:{user['password']}".encode()
        credentials = base64.b64encode(auth_data).decode('utf-8')
        response = self.app.get('/user/1/', headers={
            'Authorization': f'Basic {credentials}'})
        self.assertEqual(200, response.status_code)

    def test_put_user_successful(self):
        user = create_user(self.session)[1]
        auth_data = f"{user['user_name']}:{user['password']}".encode()
        credentials = base64.b64encode(auth_data).decode('utf-8')
        data = get_test_user_data()
        response = self.app.put('/user/1/', json=data, headers={
            'Authorization': f'Basic {credentials}'})
        self.assertEqual(200, response.status_code)

    def test_put_user_auth_error_username(self):
        user = create_user(self.session)[1]
        auth_data = f"qw:{user['password']}".encode()
        credentials = base64.b64encode(auth_data).decode('utf-8')
        response = self.app.put('/user/1/', json={'user_name': 'changed_name'}, headers={
            'Authorization': f'Basic {credentials}'})
        self.assertEqual(403, response.status_code)

    def test_put_user_error(self):
        user = create_user(self.session)[1]
        auth_data = f"{user['user_name']}:{user['password']}".encode()
        credentials = base64.b64encode(auth_data).decode('utf-8')
        response = self.app.put('/user/2/', json={'user_name': 'changed_name'}, headers={
            'Authorization': f'Basic {credentials}'})
        self.assertEqual(403, response.status_code)

    def test_delete_user_successful(self):
        user = create_user(self.session)[1]
        auth_data = f"{user['user_name']}:{user['password']}".encode()
        credentials = base64.b64encode(auth_data).decode('utf-8')
        response = self.app.delete('/user/1/', headers={
            'Authorization': f'Basic {credentials}'})
        self.assertEqual(200, response.status_code)

    def test_delete_user_not_found(self):
        user = create_user(self.session)[1]
        auth_data = f"{user['user_name']}:{user['password']}".encode()
        credentials = base64.b64encode(auth_data).decode('utf-8')
        response = self.app.delete('/user/2/', headers={
            'Authorization': f'Basic {credentials}'})
        self.assertEqual(403, response.status_code)

    def test_delete_user_successful_reservations(self):
        user = create_user(self.session)[1]
        auth_data = f"{user['user_name']}:{user['password']}".encode()
        credentials = base64.b64encode(auth_data).decode('utf-8')
        create_reservation(self.session)
        response = self.app.delete('/user/1/', headers={
            'Authorization': f'Basic {credentials}'})
        self.assertEqual(200, response.status_code)


if __name__ == '__main__':
    unittest.main()
