import unittest
from parameterized import parameterized
from my_codecs.codecs import Base64Codec

## Run with python -m unittest tests/test_codecs.py -v


class TestBase64Encoder(unittest.TestCase):
    def setUp(self):
        self.encoder = Base64Codec()

    @parameterized.expand(
        [
            [
                "Test1",
                {
                    "name": "John Doe",
                    "age": 30,
                    "contact": {"email": "john@example.com", "phone": "123-456-7890"},
                },
                {
                    "name": "Sm9obiBEb2U=",
                    "age": "MzA=",
                    "contact": "eyJlbWFpbCI6ICJqb2huQGV4YW1wbGUuY29tIiwgInBob25lIjogIjEyMy00NTYtNzg5MCJ9",
                },
            ],
            [
                "Test 2",
                {
                    "name": "John Doe",
                    "age": 30,
                    "contact": {"email": "john@example.com", "phone": "123-456-7890"},
                    "birth_date": "1998-11-19",
                },
                {
                    "name": "Sm9obiBEb2U=",
                    "age": "MzA=",
                    "contact": "eyJlbWFpbCI6ICJqb2huQGV4YW1wbGUuY29tIiwgInBob25lIjogIjEyMy00NTYtNzg5MCJ9",
                    "birth_date": "MTk5OC0xMS0xOQ==",
                },
            ],
        ]
    )
    def test_base64_encode(self, name, input_data, expected_output):
        encoded = self.encoder.encrypt(input_data)
        self.assertEqual(encoded, expected_output)

    @parameterized.expand(
        [
            [
                "Test1",
                {
                    "name": "Sm9obiBEb2U=",
                    "age": "MzA=",
                    "contact": "eyJlbWFpbCI6ICJqb2huQGV4YW1wbGUuY29tIiwgInBob25lIjogIjEyMy00NTYtNzg5MCJ9",
                },
                {
                    "name": "John Doe",
                    "age": 30,
                    "contact": {"email": "john@example.com", "phone": "123-456-7890"},
                },
            ],
            [
                "Test 2",
                {
                    "name": "Sm9obiBEb2U=",
                    "age": "MzA=",
                    "contact": "eyJlbWFpbCI6ICJqb2huQGV4YW1wbGUuY29tIiwgInBob25lIjogIjEyMy00NTYtNzg5MCJ9",
                    "birth_date": "1998-11-19",
                    "raw_json": {"hello": "riot"},
                },
                {
                    "name": "John Doe",
                    "age": 30,
                    "contact": {"email": "john@example.com", "phone": "123-456-7890"},
                    "birth_date": "1998-11-19",
                    "raw_json": {"hello": "riot"},
                },
            ],
        ]
    )
    def test_base64_decode(self, name, input_data, expected_output):
        decoded = self.encoder.decrypt(input_data)
        self.assertEqual(decoded, expected_output)


if __name__ == "__main__":
    unittest.main()
