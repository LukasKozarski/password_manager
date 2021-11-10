import base64
import json
import os
import requests
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from settings import API_URL


class PasswordManager:
    def __init__(self, passwords_file, key):
        self.key = coding_key_to_bytes(key)
        self.passwords_file = passwords_file
        self.passwords_dict = {}
        # Obiekt kryptograficzny służący do kodowania hasła
        self.coder = Fernet(self.key)

    def run(self, target, user):
        """
        Główna metoda uruchamiająca generowanie i/lub wyświetlanie hasła.
        """
        # Odczytaj zapisane w pliku zakodowane hasła
        self.read_passwords_storage()
        # Jeżeli nie ma jeszcze hasła dla podanej domeny i użytkownika, wygeneruj hasło
        if not self.passwords_dict.get(target, {}).get(user):
            self.generate_password(target, user)
        # Odczytaj hasło dla domeny i użytkownika
        self.decrypt_password(target, user)

    def read_passwords_storage(self):
        """
        Metoda odczytująca z pliku dane do logowania i zakodowane hasła.
        """
        # Jeżeli plik z hasłami nie istnieje, stwórz plik json z pustym słownikiem.
        if not os.path.exists(self.passwords_file):
            with open(self.passwords_file, 'w') as file:
                json.dump({}, file)
        # Odczytaj zawartość pliku z hasłami
        with open(self.passwords_file, 'r') as file:
            self.passwords_dict = json.load(file)

    def generate_password(self, target, user):
        """
        Metoda generująca hasło.
        """
        # Pobierz hasło z API
        generated_password = requests.get(API_URL).text
        # Zakoduj hasło
        encrypted_generated_password = self.coder.encrypt(generated_password.encode()).decode()
        # Jeżeli dla domeny nie ma jeszcze miejsca na hasła, stwórz pusty słownik
        if not self.passwords_dict.get(target):
            self.passwords_dict[target] = {}
        # Zapisz wygenerowane hasło w słowniku
        self.passwords_dict[target][user] = encrypted_generated_password
        # Zaktualizuj plik z hasłami
        with open(self.passwords_file, 'w') as file:
            json.dump(self.passwords_dict, file)

    def decrypt_password(self, target, user):
        """
        Metoda odkodowująca hasło.
        """
        # Odczytaj hasło ze słownika
        _p = self.passwords_dict[target][user]
        # Odkoduj hasło
        decrypted_password = self.coder.decrypt(_p.encode()).decode()
        # Wypisz informacje o danych logowania i haśle
        print(f"Password for: {target}/{user} is '{decrypted_password}'")


# Metoda pomocnicza, służy do generowania klucza do kodowania haseł
def coding_key_to_bytes(coding_key):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'safe-salt',
        iterations=10000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(coding_key.encode()))
    return key
