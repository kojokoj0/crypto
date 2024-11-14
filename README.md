## Python file encryption and decryption using a generated key with fernet, or a password based key using PBKDF2

### Requirements:
- ****cryptography installed****
- ****python file located in the same folder as the file you want to encrypt/decrypt****

### Usage:
- Generate key:
  ```
  python crypto.py filename -g
  ```
- Encrypt file with generated key:
  ```
  python crypto.py filename -k
  ```
- Decrypt file with generated key:
  ```
  python crypto.py filename -d
  ```
__________________________________________________________________

- Generate password based key:
  ```
  python crypto.py filename -p
  ```
- Encrypt file with password based key:
  ```
  python crypto.py filename -pk
  ```
- Decrypt file with password based key:
  ```
  python crypto.py filename -pd
  ```

