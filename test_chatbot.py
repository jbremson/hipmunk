import unittest
from src.chatbot import app, ResponseManager, invalid_response, geolocate, get_url, weather
import json

class ChatbotTestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_basic(self):
        retval = self.app.post("/chat/messages", data=dict(action='join', user_id=1234, name='joel'),
                                                            content_type='multipart/form-data')
        self.assertEqual(retval.status_code, 200)
        retval = json.loads(retval.data)
        self.assertTrue(len(retval['messages']) == 1)

    def test_ResponseManager(self):
        response_manager = ResponseManager()
        response_manager.add_response('text',' response 1')
        response_manager.add_response('text', 'response 2')
        retval = json.loads(response_manager.return_response_json())
        self.assertTrue(len(retval['messages']) == 2)

    def test_invalid_response(self):
        retval = json.loads(invalid_response("test invalid_response"))
        self.assertEqual(retval['messages'][0]['text'], "ERROR: test invalid_response")

    def test_get_url(self):
        retval = str(get_url("http://www.google.com"))
        self.assertTrue('Search' in retval)
        retval = json.loads((get_url("http://www.ljslfkjsd flksdjf lksdjfsd.com", debug=True)))
        self.assertTrue('ERROR' in retval['messages'][0]['text'])

    def test_geolocate(self):
        loc = geolocate("Los Angeles,   CA")
        self.assertTrue('lng' in loc.keys())

    def test_weather(self):
        loc = geolocate("Davis, CA")
        out = weather(loc)
        print(out)



if __name__ == '__main__':
    unittest.main()