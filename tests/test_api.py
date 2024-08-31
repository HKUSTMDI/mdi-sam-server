import unittest
from flask import Flask, json
import os, sys
from dotenv import load_dotenv
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from mdi_sam_server.label_studio_ml_mdi.api import init_app
from mdi_sam_server.sam_backend.model import SamMLBackend

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
        self.app = init_app(SamMLBackend)
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
        
    def test_health(self):
        data = {
            "task_id": "1",
            "url": "https://mdi.hkust-gz.edu.cn/images/data-manager/dogs.jpeg",
            "img_type": "normal"
        }
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['code'], 200)
        self.assertEqual(response_data['msg'], 'ok')
        

    def test_predict_normal(self):
        data = {
            "tasks": [
                {
                    "data": {
                        "image": "https://mdi.hkust-gz.edu.cn/images/data-manager/dogs.jpeg"
                    }
                }
            ],
            "model_version": "mobile_sam",
            "task_id": 1,
            "params": {
                "login": None,
                "password": None,
                "context": {
                    "result": [
                            {
                            "original_width": 880,
                            "original_height": 718,
                            "image_rotation": 0,
                            "value": {
                                "x": 50,
                                "y": 50,
                                "width": 0.3189792663476874,    
                                "keypointlabels": ["Banana"]
                            },
                            "is_positive": True,
                            "type": "keypointlabels",
                            "origin": "manual"
                        },
                        {
                            "original_width": 3840,
                            "original_height": 2160,
                            "image_rotation": 0,
                            "value": {
                                "x": 44,
                                "y": 50,
                                "width": 0.3189792663476874,    
                                "keypointlabels": ["Banana"]
                            },
                            "is_positive": True,
                            "type": "keypointlabels",
                            "origin": "manual"
                        },
                        {
                            "original_width": 3840,
                            "original_height": 2160,
                            "image_rotation": 0,
                            "value": {
                                "x": 50,
                                "y": 40,
                                "width": 0.3189792663476874,    
                                "keypointlabels": ["Banana"]
                            },
                            "is_positive": True,
                            "type": "keypointlabels",
                            "origin": "manual"
                        }
                    ]
                }
            }
        }
        response = self.client.post('/api/predict', json=data)
        self.assertEqual(response.status_code, 200)

    def test_predict_sdpc(self):
        data = {
            "tasks": [
                {
                    "data": {
                        "image": "https://mdi.hkust-gz.edu.cn/wsi/sdpc/api/sliceInfo/sdpc/20211025_065925_0%238_11"
                    }
                }
            ],
            "model_version": "sam",
            "task_id": 1,
            "img_type": "sdpc", #wsi预测需要传:sdpc/svs/tiff,
            "params": {
                "login": None,
                "password": None,
                "context": {
                    "cur_scale":1.1, #wsi预测需要传
                    "result": [
                        #画框
                        {
                            "original_width": 40320,
                            "original_height": 45696,
                            "image_rotation": 0,
                            "value": {
                                "x": 67.65,
                                "y": 37.3,
                                "width": 0.2,
                                "height": 0.2,
                                "rectanglelabels": ["Banana"]
                            },
                            "type": "rectanglelabels",
                            "origin": "manual"
                        },
                        #画positive点
                        {
                            "original_width": 3840,
                            "original_height": 2160,
                            "image_rotation": 0,
                            "value": {
                                "x": 67.72,
                                "y": 37.36,
                                "width": 0.2,
                                "keypointlabels": ["Banana"]
                            },
                            "is_positive":True,
                            "type": "keypointlabels",
                            "origin": "manual"
                        },
                        #画positive点
                        {
                            "original_width": 3840,
                            "original_height": 2160,
                            "image_rotation": 0,
                            "value": {
                                "x": 67.71,
                                "y": 37.45,
                                "width": 0.2,
                                "keypointlabels": ["Banana"]
                            },
                            "is_positive":True,
                            "type": "keypointlabels",
                            "origin": "manual"
                        },
                        #画negative点
                        {
                            "original_width": 3840,
                            "original_height": 2160,
                            "image_rotation": 0,
                            "value": {
                                "x": 67.8,
                                "y": 37.41,
                                "width": 0.3,
                                "keypointlabels": ["Banana"]
                            },
                            "is_positive":True,
                            "type": "keypointlabels",
                            "origin": "manual"
                        }

                    ]
                }
            }
        }
        response = self.client.post('/api/predict', json=data)
        self.assertEqual(response.status_code, 200)


    def test_preload_normal(self):
        data = {
            "task_id": "1",
            "url": "https://mdi.hkust-gz.edu.cn/images/data-manager/dogs.jpeg",
            "img_type": "normal"
        }
        response = self.client.post('/api/preload', json=data)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['code'], 200)




if __name__ == '__main__':
    env_path = "../.env"
    if os.path.exists(env_path):
        load_dotenv(dotenv_path=env_path)
        unittest.main()
    else:
        print("please init .env file!")
