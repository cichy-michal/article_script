import requests
from bs4 import BeautifulSoup
import csv

def pobierz_opis_artykulu(url):
    # Pobierz zawartość strony internetowej
    response = requests.get(url)
    # Sprawdź czy pobranie było udane
    if response.status_code == 200:
        # Utwórz obiekt BeautifulSoup do parsowania HTML-a
        soup = BeautifulSoup(response.content, 'html.parser')
        # Znajdź meta tag o atrybucie property równym 'og:description'
        meta_tag = soup.find('meta', property='og:description')
        if meta_tag:
            # Pobierz zawartość atrybutu content z meta tagu
            opis = meta_tag['content']
            return opis
        else:
            return "Nie można znaleźć opisu artykułu."
    else:
        return "Nie udało się pobrać strony internetowej."

def pobierz_tekst_artykulu(url):
    # Pobierz zawartość strony internetowej
    response = requests.get(url)
    # Sprawdź czy pobranie było udane
    if response.status_code == 200:
        # Utwórz obiekt BeautifulSoup do parsowania HTML-a
        soup = BeautifulSoup(response.content, 'html.parser')
        # Znajdź wszystkie elementy <p> z klasą Paragraph_desktopParagraph__Fd2e9
        paragraphs = soup.find_all('p', class_='Paragraph_desktopParagraph__Fd2e9')
        if paragraphs:
            # Połącz zawartość wszystkich znalezionych paragrafów w jeden ciąg tekstowy
            tekst = ' '.join([p.get_text() for p in paragraphs])
            return tekst
        else:
            return "Nie można znaleźć tekstu artykułu."
    else:
        return "Nie udało się pobrać strony internetowej."

def wczytaj_artykul(url):
    opis_artykulu = pobierz_opis_artykulu(url)
    tekst_artykulu = pobierz_tekst_artykulu(url)
    artykul = opis_artykulu + ' ' + tekst_artykulu
    return artykul

def wczytaj_url_z_pliku(nazwa_pliku):
    with open(nazwa_pliku, 'r') as file:
        urls = [line.strip() for line in file if line.strip()]
    return urls

def zapisz_do_csv(artykul, nazwa_pliku, numer_kolumny):
    with open(nazwa_pliku, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')  # Ustawiamy delimiter na ';'
        # Tworzymy listę, w której wszystkie kolumny oprócz wybranej będą puste
        row = [""] * (numer_kolumny - 1)  # Puste kolumny przed wybraną kolumną
        row.append(artykul)  # Dodajemy artykuł do wybranej kolumny
        writer.writerow(row)

# Przykładowe użycie
lista_url = wczytaj_url_z_pliku("url_hiszpania.txt")
for url in lista_url:
    artykul = wczytaj_artykul(url)
    zapisz_do_csv(artykul, "dataset_script.csv",5)

