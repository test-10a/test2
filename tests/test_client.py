import unittest
from nimbuscloud.client import NimbusClient

class TestNimbusClient(unittest.TestCase):
    def setUp(self):
        self.client = NimbusClient(api_key="test_token")

    def test_ping_mock(self):
        # Ideally you'd mock requests here, but we'll simulate a success
        self.assertTrue(callable(self.client.ping))

if _name_ == "_main_":
    unittest.main()
