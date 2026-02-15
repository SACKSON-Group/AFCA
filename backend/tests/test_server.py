import json
import threading
import time
import unittest
from urllib import request

from backend.server import run


class ServerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.thread = threading.Thread(target=run, kwargs={"host": "127.0.0.1", "port": 8765}, daemon=True)
        cls.thread.start()
        time.sleep(0.4)

    def test_health(self):
        with request.urlopen("http://127.0.0.1:8765/health") as res:
            self.assertEqual(res.status, 200)
            payload = json.loads(res.read().decode())
            self.assertEqual(payload["status"], "ok")

    def test_providers(self):
        with request.urlopen("http://127.0.0.1:8765/api/providers") as res:
            self.assertEqual(res.status, 200)
            payload = json.loads(res.read().decode())
            self.assertGreaterEqual(payload["count"], 1)


if __name__ == "__main__":
    unittest.main()
