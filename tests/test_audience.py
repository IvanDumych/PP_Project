import base64
import unittest

from tests.test_base import TestBase
from tests.utils import (
    create_user, get_test_user_data,
    create_audience, get_test_audience_data)


class TestAudience(TestBase):
    def test_post_audience_successful(self):
        user = create_user(self.session)[1]
        auth_data = f"{user['user_name']}:{user['password']}".encode()
        credentials = base64.b64encode(auth_data).decode('utf-8')
        audience = get_test_audience_data()
        response = self.app.post('/audience/', json=audience, headers={
            'Authorization': f'Basic {credentials}'})
        self.assertEqual(200, response.status_code)

    def test_post_audience_invalid_input_first(self):
        user = create_user(self.session)[1]
        auth_data = f"{user['user_name']}:{user['password']}".encode()
        credentials = base64.b64encode(auth_data).decode('utf-8')
        audience = get_test_audience_data()
        audience['error'] = 'error'
        response = self.app.post('/audience/', json=audience, headers={
            'Authorization': f'Basic {credentials}'})
        self.assertEqual(405, response.status_code)

    def test_post_audience_invalid_input_second(self):
        user = create_user(self.session)[1]
        auth_data = f"{user['user_name']}:{user['password']}".encode()
        credentials = base64.b64encode(auth_data).decode('utf-8')
        audience = get_test_audience_data()
        audience['size'] = -1
        response = self.app.post('/audience/', json=audience, headers={
            'Authorization': f'Basic {credentials}'})
        self.assertEqual(405, response.status_code)

    def test_get_audience_successful(self):
        user = create_user(self.session)[1]
        auth_data = f"{user['user_name']}:{user['password']}".encode()
        credentials = base64.b64encode(auth_data).decode('utf-8')
        create_audience(self.session)
        response = self.app.get('/audience/1/', headers={
            'Authorization': f'Basic {credentials}'})
        self.assertEqual(200, response.status_code)

    def test_get_audience_not_found(self):
        user = create_user(self.session)[1]
        auth_data = f"{user['user_name']}:{user['password']}".encode()
        credentials = base64.b64encode(auth_data).decode('utf-8')
        create_audience(self.session)
        response = self.app.get('/audience/2/', headers={
            'Authorization': f'Basic {credentials}'})
        self.assertEqual(403, response.status_code)

    def test_get_audiences_successful(self):
        user = create_user(self.session)[1]
        auth_data = f"{user['user_name']}:{user['password']}".encode()
        credentials = base64.b64encode(auth_data).decode('utf-8')
        create_audience(self.session)
        response = self.app.get('/audience/', headers={
            'Authorization': f'Basic {credentials}'})
        self.assertEqual(200, response.status_code)

    def test_get_audiences_not_found(self):
        user = create_user(self.session)[1]
        auth_data = f"{user['user_name']}:{user['password']}".encode()
        credentials = base64.b64encode(auth_data).decode('utf-8')
        response = self.app.get('/audience/', headers={
            'Authorization': f'Basic {credentials}'})
        self.assertEqual(403, response.status_code)


if __name__ == '__main__':
    unittest.main()
