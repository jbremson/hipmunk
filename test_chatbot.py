import unittest
import src.chatbot as chatbot

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        chatbot.app.testing = True
        self.app = chatbot.app.test_client()

    def test_basic(self):
        retval = self.app.post("/chat/messages", data=dict(action='join', user_id=1234, name='joel'),
                                                            content_type='multipart/form-data')
        self.assertEqual(retval.status_code, 200)

if __name__ == '__main__':
    unittest.main()