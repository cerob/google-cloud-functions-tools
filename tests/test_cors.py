import unittest

from src import cors


class TestCors(unittest.TestCase):

    def setUp(self):

        class DummyRequest():

            def __init__(self, method) -> None:
                self.method = method

        self.request_options = DummyRequest(method='OPTIONS')
        self.request_get = DummyRequest(method='GET')

    def test_cors_options(self):

        @cors
        def cloud_func(request):
            return 'response_text'

        res = cloud_func(self.request_options)

        self.assertEqual(res[0], '')  # For 204, should be empty
        self.assertEqual(res[1], 204)
        self.assertIsInstance(res[2], dict)
        self.assertIn('Access-Control-Allow-Origin', res[2])
        self.assertIn('Access-Control-Allow-Methods', res[2])
        self.assertNotIn('Access-Control-Allow-Headers', res[2])
        self.assertIn('Access-Control-Max-Age', res[2])

    def test_cors_options_complete_arguments(self):

        @cors(origin='sample_origin',
              methods='POST',
              headers='Content-Type',
              max_age=9600)
        def cloud_func(request):
            return 'response_text'

        res = cloud_func(self.request_options)

        self.assertEqual(res[0], '')  # For 204, should be empty
        self.assertEqual(res[1], 204)
        self.assertIsInstance(res[2], dict)
        self.assertIn('Access-Control-Allow-Origin', res[2])
        self.assertIn('Access-Control-Allow-Methods', res[2])
        self.assertIn('Access-Control-Allow-Headers', res[2])
        self.assertIn('Access-Control-Max-Age', res[2])
        self.assertEqual(res[2]['Access-Control-Allow-Origin'], 'sample_origin')
        self.assertEqual(res[2]['Access-Control-Allow-Methods'], 'POST')
        self.assertEqual(res[2]['Access-Control-Allow-Headers'], 'Content-Type')
        self.assertEqual(res[2]['Access-Control-Max-Age'], 9600)

    def test_cors_options_partial_arguments(self):

        @cors(origin='sample_origin',
              methods='POST',
              headers=None,
              max_age=None)
        def cloud_func(request):
            return 'response_text'

        res = cloud_func(self.request_options)

        self.assertEqual(res[0], '')  # For 204, should be empty
        self.assertEqual(res[1], 204)
        self.assertIsInstance(res[2], dict)
        self.assertIn('Access-Control-Allow-Origin', res[2])
        self.assertIn('Access-Control-Allow-Methods', res[2])
        self.assertNotIn('Access-Control-Allow-Headers', res[2])
        self.assertNotIn('Access-Control-Max-Age', res[2])
        self.assertEqual(res[2]['Access-Control-Allow-Origin'], 'sample_origin')
        self.assertEqual(res[2]['Access-Control-Allow-Methods'], 'POST')

    def test_cors_len_3_tuple_returns(self):

        @cors
        def cloud_func(request):
            return 'response_text', 200, {'Origin': 'localhost'}

        res = cloud_func(self.request_get)

        self.assertEqual(res[0], 'response_text')
        self.assertEqual(res[1], 200)
        self.assertIsInstance(res[2], dict)
        self.assertIn('Origin', res[2])
        self.assertIn('Access-Control-Allow-Origin', res[2])
        self.assertIn('Access-Control-Allow-Methods', res[2])
        self.assertNotIn('Access-Control-Allow-Headers', res[2])
        self.assertIn('Access-Control-Max-Age', res[2])

    def test_cors_len_2_tuple_returns_with_status_code(self):

        @cors
        def cloud_func(request):
            return 'response_text', 200

        res = cloud_func(self.request_get)

        self.assertEqual(res[0], 'response_text')
        self.assertEqual(res[1], 200)
        self.assertIsInstance(res[2], dict)
        self.assertIn('Access-Control-Allow-Origin', res[2])
        self.assertIn('Access-Control-Allow-Methods', res[2])
        self.assertNotIn('Access-Control-Allow-Headers', res[2])
        self.assertIn('Access-Control-Max-Age', res[2])

    def test_cors_len_2_tuple_returns_with_some_headers(self):

        @cors
        def cloud_func(request):
            return 'response_text', {'Origin': 'localhost'}

        res = cloud_func(self.request_get)

        self.assertEqual(res[0], 'response_text')
        self.assertIsInstance(res[1], dict)
        self.assertIn('Origin', res[1])
        self.assertIn('Access-Control-Allow-Origin', res[1])
        self.assertIn('Access-Control-Allow-Methods', res[1])
        self.assertNotIn('Access-Control-Allow-Headers', res[1])
        self.assertIn('Access-Control-Max-Age', res[1])

    def test_cors_len_1_tuple_returns(self):

        @cors
        def cloud_func(request):
            return ('response_text',)

        res = cloud_func(self.request_get)

        self.assertEqual(res[0], 'response_text')
        self.assertIsInstance(res[1], dict)
        self.assertIn('Access-Control-Allow-Origin', res[1])
        self.assertIn('Access-Control-Allow-Methods', res[1])
        self.assertNotIn('Access-Control-Allow-Headers', res[1])
        self.assertIn('Access-Control-Max-Age', res[1])

    def test_cors_string_or_object_returns(self):

        @cors
        def cloud_func(request):
            return 'response_text'

        res = cloud_func(self.request_get)

        self.assertEqual(res[0], 'response_text')
        self.assertIsInstance(res[1], dict)
        self.assertIn('Access-Control-Allow-Origin', res[1])
        self.assertIn('Access-Control-Allow-Methods', res[1])
        self.assertNotIn('Access-Control-Allow-Headers', res[1])
        self.assertIn('Access-Control-Max-Age', res[1])


if __name__ == '__main__':
    unittest.main()
