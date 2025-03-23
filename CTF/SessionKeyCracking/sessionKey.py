import hmac
import hashlib
from binascii import unhexlify
from Crypto.Cipher import ARC4
import sys

def get_response_key_nt(nt_hash, user, domain):
    user_domain = (user.upper() + domain.upper()).encode('utf-16le')
    return hmac.new(nt_hash, user_domain, hashlib.md5).digest()

def get_key_exchange_key(response_key_nt, nt_proof_str):
    return hmac.new(response_key_nt, nt_proof_str, hashlib.md5).digest()

def decrypt_session_key(key_exchange_key, encrypted_session_key):
    rc4 = ARC4.new(key_exchange_key)
    return rc4.decrypt(encrypted_session_key)

def main():
    if len(sys.argv) < 5 or len(sys.argv) > 7:
        print("Usage for NT hash method: python script.py nt_hash username domain nt_hash_value NTProofStr EncryptedSessionKey")
        print("Usage for password method: python script.py password username domain password_value NTProofStr EncryptedSessionKey")
        sys.exit(1)

    method = sys.argv[1]
    user = sys.argv[2]
    domain = sys.argv[3]
    
    if method == 'nt_hash':
        if len(sys.argv) != 7:
            print("Usage: python script.py nt_hash username domain nt_hash_value NTProofStr EncryptedSessionKey")
            sys.exit(1)
        
        try:
            nt_hash = unhexlify(sys.argv[4])
            NTProofStr = unhexlify(sys.argv[5])
            EncryptedSessionKey = unhexlify(sys.argv[6])
        except Exception as e:
            print(f"Error parsing hex values: {e}")
            sys.exit(1)

        response_key_nt = get_response_key_nt(nt_hash, user, domain)
        print(f"ResponseKeyNT: {response_key_nt.hex()}")

        key_exchange_key = get_key_exchange_key(response_key_nt, NTProofStr)
        print(f"KeyExchangeKey: {key_exchange_key.hex()}")

        random_session_key = decrypt_session_key(key_exchange_key, EncryptedSessionKey)
        print(f"RandomSessionKey: {random_session_key.hex()}")

    elif method == 'password':
        if len(sys.argv) != 7:
            print("Usage: python script.py password username domain password_value NTProofStr EncryptedSessionKey")
            sys.exit(1)

        password = sys.argv[4]
        try:
            NTProofStr = unhexlify(sys.argv[5])
            EncryptedSessionKey = unhexlify(sys.argv[6])
        except Exception as e:
            print(f"Error parsing hex values: {e}")
            sys.exit(1)

        # Step 1: MD4 hash of the password
        try:
            md4_hash = hashlib.new('md4', password.encode('utf-16le')).digest()
        except Exception as e:
            print(f"Error hashing password: {e}")
            sys.exit(1)

        print(f"MD4 Hash of Password: {md4_hash.hex()}")

        # Step 2: Calculate ResponseKeyNT using HMAC-MD5
        response_key_nt = get_response_key_nt(md4_hash, user, domain)
        print(f"ResponseKeyNT: {response_key_nt.hex()}")

        # Step 3: Calculate KeyExchangeKey using HMAC-MD5
        key_exchange_key = get_key_exchange_key(response_key_nt, NTProofStr)
        print(f"KeyExchangeKey: {key_exchange_key.hex()}")

        # Step 4: Decrypt EncryptedSessionKey using RC4
        random_session_key = decrypt_session_key(key_exchange_key, EncryptedSessionKey)
        print(f"RandomSessionKey: {random_session_key.hex()}")

    else:
        print("Invalid method. Use 'nt_hash' or 'password'.")

if __name__ == "__main__":
    main()
