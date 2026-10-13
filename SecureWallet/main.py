"""Demo lokal SecureWallet. Tidak digunakan untuk uang sungguhan."""
import base64
import json
import secrets
from datetime import datetime, timezone
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.exceptions import InvalidSignature


def canonical_json(data: dict) -> bytes:
    """Representasi deterministik untuk objek JSON berisi data transaksi."""
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def create_key_pair():
    """Buat RSA key pair; randomness ditangani pustaka cryptography."""
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    return private_key, private_key.public_key()


def make_transaction(sender: str, receiver: str, amount: int) -> dict:
    if not sender.strip() or not receiver.strip():
        raise ValueError("Pengirim dan penerima wajib diisi.")
    if sender == receiver:
        raise ValueError("Pengirim dan penerima harus berbeda.")
    if not isinstance(amount, int) or isinstance(amount, bool) or amount <= 0:
        raise ValueError("Nominal harus berupa bilangan bulat positif.")
    return {
        "transaction_id": secrets.token_hex(8),
        "sender": sender,
        "receiver": receiver,
        "amount": amount,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "nonce": secrets.token_hex(16),
    }


def sign_transaction(transaction: dict, private_key) -> str:
    signature = private_key.sign(
        canonical_json(transaction),
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256(),
    )
    return base64.b64encode(signature).decode("ascii")


def verify_transaction(transaction: dict, signature_b64: str, public_key) -> bool:
    try:
        signature = base64.b64decode(signature_b64, validate=True)
        public_key.verify(
            signature,
            canonical_json(transaction),
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256(),
        )
        return True
    except (InvalidSignature, ValueError, TypeError):
        return False


def audit_entry(transaction: dict, signature_b64: str, previous_hash: str) -> dict:
    payload = {
        "transaction": transaction,
        "signature": signature_b64,
        "previous_hash": previous_hash,
    }
    entry_hash = hashes.Hash(hashes.SHA256())
    entry_hash.update(canonical_json(payload))
    payload["entry_hash"] = entry_hash.finalize().hex()
    return payload


def verify_audit_chain(entries: list) -> bool:
    previous_hash = "GENESIS"
    for entry in entries:
        if entry.get("previous_hash") != previous_hash:
            return False
        payload = {k: entry[k] for k in ("transaction", "signature", "previous_hash")}
        digest = hashes.Hash(hashes.SHA256())
        digest.update(canonical_json(payload))
        if digest.finalize().hex() != entry.get("entry_hash"):
            return False
        previous_hash = entry["entry_hash"]
    return True


def main():
    private_key, public_key = create_key_pair()
    tx = make_transaction("alice_demo", "bob_demo", 250)
    signature = sign_transaction(tx, private_key)
    print("SecureWallet — simulasi transaksi")
    print("Transaksi:", json.dumps(tx, indent=2, ensure_ascii=False))
    print("Tanda tangan valid:", verify_transaction(tx, signature, public_key))
    altered = dict(tx)
    altered["amount"] = 999999
    print("Transaksi setelah nominal diubah valid:", verify_transaction(altered, signature, public_key))
    entry = audit_entry(tx, signature, "GENESIS")
    print("Rantai audit valid:", verify_audit_chain([entry]))
    # Kunci privat hanya berada di memori; jangan mencetak atau menyimpannya.


if __name__ == "__main__":
    main()
