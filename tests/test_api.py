import os
import base64
import json
import unittest
from fastapi.testclient import TestClient

# Run with python -m unittest tests/test_api.py -v

# Ensure a deterministic signing key BEFORE importing the app/providers
os.environ.setdefault("SIGNER_KEY", "test-secret")

from main import app

client = TestClient(app)


class TestAPI(unittest.TestCase):
    def test_encrypt_decrypt_roundtrip(self):
        payload = {
            "name": "John Doe",
            "age": 30,
            "contact": {"email": "john@example.com", "phone": "123-456-7890"},
            "active": True,
            "notes": None,
            "tags": ["a", "b"],
        }
        # encrypt
        r = client.post("/encrypt", json=payload)
        self.assertEqual(r.status_code, 200, r.text)
        enc = r.json()

        # ensure top-level values are strings (Base64 outputs)
        for k, v in enc.items():
            self.assertIsInstance(v, str)

        # decrypt back
        r2 = client.post("/decrypt", json=enc)
        self.assertEqual(r2.status_code, 200, r2.text)
        dec = r2.json()

        self.assertEqual(dec, payload)

    def test_decrypt_leaves_unencrypted_intact(self):
        # Build a mixed payload: some valid base64-encoded fields, and some unencrypted
        encrypted_mixed = {
            "name": base64.b64encode("John Doe".encode("utf-8")).decode("ascii"),
            "age": base64.b64encode(
                json.dumps(
                    30,
                    separators=(",", ":"),
                ).encode("utf-8")
            ).decode("ascii"),
            "contact": base64.b64encode(
                json.dumps(
                    {"email": "john@example.com", "phone": "123-456-7890"},
                    separators=(",", ":"),
                ).encode("utf-8")
            ).decode("ascii"),
            "birth_date": "1998-11-19",
            "raw_json": {"hello": "riot"},
        }
        r = client.post("/decrypt", json=encrypted_mixed)
        self.assertEqual(r.status_code, 200, r.text)
        dec = r.json()

        self.assertEqual(dec["name"], "John Doe")
        self.assertEqual(dec["age"], 30)
        self.assertEqual(
            dec["contact"], {"email": "john@example.com", "phone": "123-456-7890"}
        )
        self.assertEqual(dec["birth_date"], "1998-11-19")
        self.assertEqual(dec["raw_json"], {"hello": "riot"})

    def test_sign_and_verify_success(self):
        data = {"message": "Hello World", "timestamp": 1616161616}
        r = client.post("/sign", json=data)
        self.assertEqual(r.status_code, 200, r.text)
        sig = r.json()["signature"]
        self.assertTrue(isinstance(sig, str) and len(sig) > 0)

        r2 = client.post("/verify", json={"signature": sig, "data": data})
        self.assertEqual(r2.status_code, 204, r2.text)

    def test_sign_order_independence(self):
        a = {"message": "Hello World", "timestamp": 1616161616}
        b = {"timestamp": 1616161616, "message": "Hello World"}

        r1 = client.post("/sign", json=a)
        self.assertEqual(r1.status_code, 200, r1.text)
        r2 = client.post("/sign", json=b)
        self.assertEqual(r2.status_code, 200, r2.text)

        self.assertEqual(r1.json()["signature"], r2.json()["signature"])

        # Verify the signature against differently ordered data
        sig = r1.json()["signature"]
        r3 = client.post("/verify", json={"signature": sig, "data": b})
        self.assertEqual(r3.status_code, 204, r3.text)

    def test_verify_failure_on_tamper(self):
        data = {"message": "Hello World", "timestamp": 1616161616}
        sig = client.post("/sign", json=data).json().get("signature")
        self.assertTrue(isinstance(sig, str) and len(sig) > 0)

        tampered = {"message": "Goodbye World", "timestamp": 1616161616}
        r = client.post("/verify", json={"signature": sig, "data": tampered})
        self.assertEqual(r.status_code, 400)
        self.assertIn("Invalid signature", r.text)


if __name__ == "__main__":
    unittest.main()
