import argparse
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet, InvalidToken
import os, os.path
import base64

def passwordKey(): # Funktion: genererar en lösenordsbaserad nyckel
    passwordInput = input('Var god och ange lösenord: ') 
    password = passwordInput.encode()
    usersalt = os.urandom(16)  
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=usersalt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password)) 
    with open('passKey.key', 'wb') as key4file:
        key4file.write(key)

def callPassKey(): # Funktion kallar på nyckeln för användning av kryptering/dekryptering
    try:
        return open('passKey.key', 'rb').read()
    except FileNotFoundError:
        print('Ingen lösenordsbaserad nyckel hittades')

def keyFileCheck(keyFile): # Funktion, kollar om en genererad nyckel existerar och isåfall ger användaren alternativ. Annars genereras en nyckel
    if os.path.exists(keyFile):
        varning = input('VARNING! En genererad nyckel existerar redan.\nOm du genererar en ny nyckel, och har krypterat en fil utan att dekryptera den kan du gå måste om din fil.\nVill du fortsätta? [j] för att fortsätta, [n] för att gå tillbaka\n').lower()
        if varning == 'j' and keyFile == 'key.key':
            generator()
        elif varning == 'j' and keyFile == 'passKey.key':
            passwordKey()
        elif varning == 'n':
            print('Återgår till startsidan')
        else:
            print('Felaktigt val, återgår till startsidan')
    elif not os.path.exists(keyFile) and keyFile == 'key.key':
        generator()
    elif not os.path.exists(keyFile) and keyFile == 'passKey.key':
        passwordKey()

def generator(): #Funktion: Generera nyckel
    key = Fernet.generate_key() 
    with open('key.key', 'wb') as key4file:
        key4file.write(key)

def callKey(): # Funktion kallar på nyckeln för användning av kryptering/dekryptering
    try:
        return open('key.key', 'rb').read()
    except FileNotFoundError:
        print('Ingen nyckel hittades')

def encryption(fileName, key): # Funktion: Kryptera fil 
    try:        
        f = Fernet(key)
        with open(fileName, 'rb') as file:
            content = file.read()
        contentEncrypted = f.encrypt(content)
        with open(fileName, 'wb') as file:
            file.write(contentEncrypted)
    except FileNotFoundError:
        print('Filen hittades inte')
    except TypeError:
        print('Kommandot kördes inte, kontrollera att det finns en genererad nyckel')

def decryption(fileName, key): # Funktion: Dekryptera fil
    try:
        f = Fernet(key)
        with open(fileName, 'rb') as file:
            contentEncrypted = file.read()
        contentDecrypted = f.decrypt(contentEncrypted)
        with open(fileName, 'wb') as file:
            file.write(contentDecrypted)
    except FileNotFoundError:
        print('Filen hittades inte')
    except TypeError:
        print('Kommandot kördes inte, kontrollera att det finns en genererad nyckel')
    except InvalidToken:
        print('Nyckeln för kryptering matchar inte nyckeln för dekryptering')

parser = argparse.ArgumentParser(description='Generera nyckel/Kryptera/Dekryptera')
parser.add_argument('file', help='Fil för kryptering/dekryptering')
parser.add_argument('-g', '--generera', action='store_true', help='Generera nyckel')
parser.add_argument('-k', '--kryptera', action='store_true', help='Kryptera angiven fil')
parser.add_argument('-d', '--dekryptera', action='store_true', help='Dekryptera angiven fil')
parser.add_argument('-p', '--password', action='store_true', help='Ange lösenord för att generera lösenordsbaserad nyckel')
parser.add_argument('-pk', '--passwordKryptering', action='store_true', help='Kryptera med lösenordsbaserad nyckel')
parser.add_argument('-pd', '--passwordDekryptering', action='store_true', help='Dekryptera med lösenordsbaserad nyckel')
args = parser.parse_args()

if args.generera:
    keyFileCheck('key.key')

elif args.password:
    keyFileCheck('passKey.key')

elif args.kryptera:
    key = callKey()
    encryption(args.file, key)

elif args.dekryptera:
    key = callKey()
    decryption(args.file, key)

elif args.passwordKryptering:
    key = callPassKey()
    encryption(args.file, key)

elif args.passwordDekryptering:
    key = callPassKey()
    decryption(args.file, key)


