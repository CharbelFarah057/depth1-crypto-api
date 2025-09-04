import unittest
from parameterized import parameterized
from my_signers.signers import HMAC

## Run with python -m unittest tests/test_signers.py -v


class TestHMACSigner(unittest.TestCase):
    def setUp(self):
        self.signer = HMAC("test")

    @parameterized.expand(
        [
            [
                "Test1",
                {"message": "Hello World", "timestamp": 1616161616},
                "53da33c0fbb53a7d3826e9c6f56bbf43410757c7c606470a867a55dda54f7528",
            ],
            [
                "Test2",
                {"timestamp": 1616161616, "message": "Hello World"},
                "53da33c0fbb53a7d3826e9c6f56bbf43410757c7c606470a867a55dda54f7528",
            ],
        ]
    )
    def test_hmac_sign(self, name, data, expected_signature):
        signature = self.signer.sign(data)
        self.assertEqual(signature, expected_signature)

    @parameterized.expand(
        [
            [
                "Test 1",
                "53da33c0fbb53a7d3826e9c6f56bbf43410757c7c606470a867a55dda54f7528",
                {"message": "Hello World", "timestamp": 1616161616},
            ],
            [
                "Test 2",
                "53da33c0fbb53a7d3826e9c6f56bbf43410757c7c606470a867a55dda54f7528",
                {
                    "timestamp": 1616161616,
                    "message": "Hello World",
                },
            ],
        ]
    )
    def test_hmac_verify(self, name, signature, data):
        calculated_signature = self.signer.sign(data)
        self.assertTrue(calculated_signature)


if __name__ == "__main__":
    unittest.main()
