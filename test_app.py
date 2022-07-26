import json
import unittest

from app import app, db


class CharterCompanyTestCase(unittest.TestCase):
    # setup and teardown
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://alexkzmn@localhost:5432/test_db'
        self.app = app.test_client()
        self.client = app.test_client()
        db.drop_all()
        db.create_all()

    # executed after each test
    def tearDown(self):
        pass

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_get_charters(self):
        res = self.client.get('/charters')
        self.assertEqual(res.status_code, 200)

    def test_get_charters_fail(self):
        res = self.client.get('/csharters')
        self.assertEqual(res.status_code, 404)

    def test_get_skippers(self):
        res = self.client.get('/skippers')
        self.assertEqual(res.status_code, 200)

    def test_get_skippers_fail(self):
        res = self.client.get('/slippers')
        self.assertEqual(res.status_code, 404)

    def test_create_charter(self):
        new_charter = {
            "id": 1,
            "charters_name": "Amazon",
            "departure_date": "2020/02/09"
        }

        res = self.client.post('/charters/create', json=new_charter)

        self.assertEqual(res.status_code, 200)

    def test_create_skipper(self):
        new_skipper = {
            "name": "Martin",
            "age": 46,
            "gender": "male",
            "charter_id": 1
        }

        res = self.client.post('/skippers/create', json=new_skipper)

        self.assertEqual(res.status_code, 401)

    def test_delete_charter(self):
        res = self.client().delete('/charters/delete/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_charter_fail(self):
        res = self.client().delete('/charters/delete/1000')
        self.assertEqual(res.status_code, 404)

    def test_delete_skipper(self):
        res = self.client().delete('/skippers/delete/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_skipper_fail(self):
        res = self.client().delete('/skippers/delete/1000')
        self.assertEqual(res.status_code, 404)

    def test_edit_charter(self):
        new_charter = {
            "id": 1,
            "charters_name": "Amazon",
            "departure_date": "2020/02/09"
        }
        res = self.client().patch('/charters/patch/2', new_charter)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_charter_fail(self):
        new_charter = {
            "id": 1,
            "charters_name": "Amazon",
            "departure_date": "2020/02/09"
        }
        res = self.client().patch('/charters/patch/2000', new_charter)
        self.assertEqual(res.status_code, 404)

    def test_edit_skipper(self):
        new_skipper = {
            "name": "Martin",
            "age": 46,
            "gender": "male",
            "charter_id": 1
        }
        res = self.client().patch('/skippers/patch/2', new_skipper)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_edit_skipper_fail(self):
        new_skipper = {
            "name": "Martin",
            "age": 46,
            "gender": "male",
            "charter_id": 1
        }
        res = self.client().patch('/skippers/patch/2000', new_skipper)
        self.assertEqual(res.status_code, 404)


if __name__ == "__main__":
    unittest.main()
