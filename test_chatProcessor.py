from chatProcessor import processString
import unittest
import json

class TestChatProcessor(unittest.TestCase):

    def test_empty(self):
        self.assertEqual(
            json.loads(processString('')),
            {'words': 0})

    def test_mention(self):
        self.assertEqual(
            json.loads(processString('@john hey, you around')),
            {
                "mentions": [ "john" ],
                "words": 3
            })

    def test_emoticon(self):
        self.assertEqual(
            json.loads(processString('Good morning! (smile) (coffee)')),
            {
                "emoticons": [ "smile", "coffee" ],
                "words": 2
            })

if __name__ == "__main__":
    unittest.main()
