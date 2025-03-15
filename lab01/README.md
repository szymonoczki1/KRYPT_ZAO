# Instrukcja użytkowania programu do szyfrowania i kryptoanalizy

## Przykładowe dane

- Tekst jawny: The quick brown fox jumps over 13 lazy dogs.
- Tekst zaszyfrowany dla szyfru afinicznego: Zrc kewsg npaov hat beqfu ajcp 13 lidy xamu.
- Tekst zaszyfrowany dla szyfru cezara: Ymj vznhp gwtbs ktc ozrux tajw 13 qfed itlx.
- Klucz dla szyfru afinicznego: 5 8
- Klucz dla szyfru cezara: 5

---

## Wymagania

- Python
- Pliki wejściowe: `plain.txt`, `crypto.txt`, `key.txt`, `extra.txt` (w zależności od wybranej operacji)

---

## Uruchamianie programu

```bash
python3 cezafi.py [opcje]
```

---

## Dostępne opcje

- `-h` - Pomoc
- `-c` - Użycie szyfru Cezara
- `-a` - Użycie szyfru afinicznego
- `-e` - Szyfrowanie
- `-d` - Deszyfrowanie
- `-j` - Kryptoanaliza z tekstem jawnym
- `-k` - Kryptoanaliza bez tekstu jawnego

### Przykłady wywołań

1. **Szyfrowanie szyfrem Cezara**

```bash
python cezafi.py -c -e
```

Wymagane pliki: `plain.txt`, `key.txt`

2. **Deszyfrowanie szyfrem Cezara**

```bash
python cezafi.py -c -d
```

Wymagane pliki: `crypto.txt`, `key.txt`

3. **Kryptoanaliza z tekstem jawnym (szyfr Cezara)**

```bash
python cezafi.py -c -j
```

Wymagane pliki: `crypto.txt`, `extra.txt`

4. **Kryptoanaliza bez tekstu jawnego (szyfr Cezara)**

```bash
python cezafi.py -c -k
```

Wymagane pliki: `crypto.txt`

5. **Szyfrowanie szyfrem afinicznym**

```bash
python cezafi.py -a -e
```

Wymagane pliki: `plain.txt`, `key.txt`

6. **Deszyfrowanie szyfrem afinicznym**

```bash
python cezafi.py -a -d
```

Wymagane pliki: `crypto.txt`, `key.txt`

7. **Kryptoanaliza z tekstem jawnym (szyfr afiniczny)**

```bash
python cezafi.py -a -j
```

Wymagane pliki: `crypto.txt`, `extra.txt`

8. **Kryptoanaliza bez tekstu jawnego (szyfr afiniczny)**

```bash
python cezafi.py -a -k
```

Wymagane pliki: `crypto.txt`

---

## Struktura plików

- `plain.txt` - tekst jawny do zaszyfrowania
- `crypto.txt` - zaszyfrowany tekst
- `key.txt` - klucz szyfrowania/deszyfrowania (dla Cezara: liczba, dla afinicznego: para liczb `a b`)
- `extra.txt` - dodatkowy tekst jawny do kryptoanalizy
- `key-found.txt` - plik, w którym zapisywany jest znaleziony klucz (przy kryptoanalizie z tekstem jawnym)
- `decrypt.txt` - plik z tekstem odszyfrowanym

---

## Obsługa błędów

1. Użycie zarówno szyfru Cezara, jak i afinicznego jednocześnie jest zabronione.
2. Należy wybrać dokładnie jedną operację z: `-e`, `-d`, `-j`, `-k`.
3. Program sprawdza, czy wymagane pliki istnieją. W przypadku braku plików, zostanie zgłoszony błąd.

---

## Uwagi

- Program automatycznie zapisuje wyniki w odpowiednich plikach (`crypto.txt`, `decrypt.txt`, `key-found.txt`).

---



