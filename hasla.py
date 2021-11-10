import sys
from password_manager import PasswordManager

# Wczytanie danych ze standardowego wyjscia
passwords_file = sys.argv[1]                    # <plik_zapisu_hasel (ma unikalne haslo)>
coding_key = sys.argv[2]                        # <haslo_do_kodowania>
password_target = sys.argv[3]                   # <do_czego_jest_haslo>
username = sys.argv[4]                          # <nazwa_usera>

# Inicjalizacja obiektu PasswordManager
pm = PasswordManager(passwords_file, coding_key)

# Uruchomienie procesu generowania / odczytu hasla
pm.run(password_target, username)
