import unittest
from main import (
    create_key_pair, make_transaction, sign_transaction,
    verify_transaction, audit_entry, verify_audit_chain
)


class SecureWalletTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.private_key, cls.public_key = create_key_pair()
        cls.other_private, cls.other_public = create_key_pair()
        cls.tx = make_transaction("alice_demo", "bob_demo", 250)
        cls.signature = sign_transaction(cls.tx, cls.private_key)

    def test_valid_signature_is_accepted(self):
        self.assertTrue(verify_transaction(self.tx, self.signature, self.public_key))

    def test_modified_amount_is_rejected(self):
        changed = dict(self.tx)
        changed["amount"] = 251
        self.assertFalse(verify_transaction(changed, self.signature, self.public_key))

    def test_wrong_public_key_is_rejected(self):
        self.assertFalse(verify_transaction(self.tx, self.signature, self.other_public))

    def test_zero_amount_is_rejected(self):
        with self.assertRaises(ValueError):
            make_transaction("alice_demo", "bob_demo", 0)

    def test_audit_chain_detects_tampering(self):
        entry = audit_entry(self.tx, self.signature, "GENESIS")
        self.assertTrue(verify_audit_chain([entry]))
        changed = dict(entry)
        changed["transaction"] = dict(entry["transaction"])
        changed["transaction"]["amount"] = 100000
        self.assertFalse(verify_audit_chain([changed]))


if __name__ == "__main__":
    unittest.main()
