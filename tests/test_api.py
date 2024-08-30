import unittest
from flask import Flask, json
import os, sys

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from label_studio_ml_mdi.api import init_app
from sam_backend.model import SamMLBackend

class MockModel(SamMLBackend):
    def predict(self, tasks, context=None, **kwargs):
        return [{"result": "mocked prediction"}]

    def preload(self, image_url):
        return True

    def get(self, param):
        if param == 'model_version':
            return "mock_version"

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = init_app(MockModel)
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
        
    def test_health(self):
        data = {
            "task_id": "1",
            "url": "http://example.com/image.jpg",
            "img_type": "normal"
        }
        response = self.client.post('/', json=data)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['code'], 200)
        self.assertEqual(response_data['msg'], 'ok')
        self.assertEqual(response_data['model_version'], 'mock_version')
        

    def test_predict_normal(self):
        data = {
            "task_id": "1",
            "tasks": [{"data": "task1"}],
            "img_type": "normal"
        }
        response = self.client.post('/api/predict', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('results', json.loads(response.data))

    def test_predict_sdpc(self):
        data = {
            "task_id": "1",
            "tasks": [{"data": "task1"}],
            "img_type": "sdpc"
        }
        response = self.client.post('/api/predict', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('results', json.loads(response.data))

    def test_predict_unknown_type(self):
        data = {
            "task_id": "1",
            "tasks": [{"data": "task1"}],
            "img_type": "unknown"
        }
        response = self.client.post('/api/predict', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['results'], "unkown type,please use normal/sdpc/svs/tiff file.")

    def test_preload_normal(self):
        data = {
            "task_id": "1",
            "url": "http://example.com/image.jpg",
            "img_type": "normal"
        }
        response = self.client.post('/api/preload', json=data)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['code'], 200)
        self.assertEqual(response_data['msg'], 'ok')
        self.assertEqual(response_data['model_version'], 'mock_version')



if __name__ == '__main__':
    unittest.main()
