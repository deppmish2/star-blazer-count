from handle import app
import unittest
import json

event = {
    "githubOwnerName": "deppmish2",
    "githubProjectName": "star-blazer-count"

}

class githubStarDataHandlerTestCase(unittest.TestCase):

    def test_star_data_handler(self):
        app.config['TESTING'] = True
        tester = app.test_client(self)

        # test the response with auth token, 200 expected
        response = tester.get(
            '/getStarCountData',
            data=json.dumps(event),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
