import unittest
from src.chatbot import app, ResponseManager, invalid_response, geolocate, get_url, parse_location, get_weather
import json

#TODO - remove prints. Add good integration test.
class ChatbotTestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_join(self):
        retval = self.app.post("/chat/messages", data=dict(action='join', user_id=1234, name='joel'),
                                                            content_type='multipart/form-data')
        self.assertEqual(retval.status_code, 200)
        retval = json.loads(retval.data)
        self.assertTrue(len(retval['messages']) == 1)

    def test_bad_message(self):
        retval = self.app.post("/chat/messages", data=dict(action='message', user_id=1234,
                                                           text='kjsdf kljsd f kjdsfsdfdd k'))
        retval = json.loads(retval.data)
        self.assertTrue('understand' in retval['messages'][0]['text'])


    def test_good_message(self):
        retval = self.app.post("/chat/messages", data=dict(action='message', user_id=1234,
                                                           text='what is the weather in Los Angeles'))
        retval = json.loads(retval.data)
        self.assertTrue("Currently it's" in retval['messages'][0]['text'])

    def test_ResponseManager(self):
        response_manager = ResponseManager()
        response_manager.add_response('text',' response 1')
        response_manager.add_response('text', 'response 2')
        retval = json.loads(response_manager.return_response_json())
        self.assertTrue(len(retval['messages']) == 2)

    def test_invalid_response(self):
        retval = json.loads(invalid_response("test invalid_response"))
        self.assertEqual(retval['messages'][0]['text'], "test invalid_response")

    def test_get_url(self):
        retval = str(get_url("http://www.google.com"))
        self.assertTrue('Search' in retval)
        print("\n\nError messages should be printed here.")
        retval = json.loads((get_url("http://www.ljslfkjsd flksdjf lksdjfsd.com", debug=True)))
        self.assertTrue('text' in retval['messages'][0].keys())

    def test_geolocate(self):
        loc = geolocate("Los Angeles,   CA")
        self.assertTrue('lng' in loc.keys())

    def test_weather(self):
        loc = geolocate("Davis, CA")
        out = get_weather(loc)
        self.assertTrue('summary' in out.keys())

    def test_parse_location(self):
        txt = "weather in Paris FRance"
        loc = parse_location(txt)
        self.assertEqual('paris france', loc)
        txt = "Los Angeles, CA weather"
        loc = parse_location(txt)
        self.assertEqual("los angeles, ca",loc)
        txt = "lkjsdlfkj  lkjsdfk sfjkds"
        # Convert this to exception catching test.
        caught = False
        try:
            loc = json.loads(parse_location(txt))
        except ValueError:
            caught = True
        self.assertTrue(caught)


if __name__ == '__main__':
    unittest.main()