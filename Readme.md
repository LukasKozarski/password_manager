# Działanie programu:

Program służy do generowania oraz odczytywania z dysku zakodowanych haseł.
Program uruchamiany jest z poziomu terminala za pomocą polecenia:

python hasla.py <plik_z_haslami.json> <unikalne_haslo_do_pliku> <do_czego_haslo> <username>

np. python hasla.py passwords.json SuperHaslo gmail.com MyUserName

Jeżeli plik <plik_z_haslami.json> nie istnieje, zostanie automatycznie utworzony w aktualnym katalogu podczas
generowania hasla.
Jeżeli hasło do danej domeny nie zostało jeszcze wygenerowane, zostanie automatycznie wygenerowane, wyświetlone,
zakodowane i zapisane w pliku <plik_z_haslami.json>.