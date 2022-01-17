from bs4 import BeautifulSoup
import requests
import time
import random
import csv
#from pprint import pprint


def get_col8_name(h4_tags, h4_text):
    for h4 in h4_tags:
        if h4.get_text().find(h4_text) != -1:
            mt2 = h4.parent.parent
            col8 = mt2.find("div", { "class": "col-8" })
            return col8.get_text().strip()
    return None

cenoteka_response = requests.get("https://cenoteka.rs/proizvodi/slatkisi-i-grickalice/bombone?page=3")
cenoteka_soup = BeautifulSoup(cenoteka_response.content, "lxml")
proizvodi_links = cenoteka_soup.find_all("div", {"class": "article-name"})

proizvodi = []

for div_proizvod in proizvodi_links:
    link = div_proizvod.find("a")
    if link and "href" in link.attrs:
        url = link["href"]

        proizvod_response = requests.get(f"https://cenoteka.rs{url}")
        proizvod_soup = BeautifulSoup(proizvod_response.content, "lxml")
        
        h4_tags = proizvod_soup.find_all("h4")
        proizvodjac = get_col8_name(h4_tags, "Proizvođač")
        kolicina = get_col8_name(h4_tags, "Količina i jedinica mere")
        barkod = get_col8_name(h4_tags, "Poznati bar-kodovi")
        slika = ""
        article_image = proizvod_soup.find("div", { "class": "article-image" })
        img = article_image.find("img")
        slika = img["src"]


        proizvodi.append({
            "url": f"https://cenoteka.rs{url}",
            "naziv": proizvod_soup.h1.get_text().strip(),
            "proizvodjac": proizvodjac,
            "kolicina": kolicina,
            "barkod": barkod,
            "slika": f"https://cenoteka.rs{slika}"
        })

        time.sleep(random.uniform(0.8, 1.5))

#pprint(proizvodi)

with open("data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["url", "naziv", "proizvodjac", "kolicina", "barkod", "slika"])
    for proizvod in proizvodi:
        writer.writerow(proizvod.values())