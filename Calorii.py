import requests
from bs4 import BeautifulSoup
import json
import csv

url = "https://calorii.oneden.com/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.50"
}

req = requests.get(url, headers=headers)

src = req.text
with open(f"data/index.html", "w") as file:
    file.write(src)

with open(f"data/index.html") as file:
    src = file.read()

    soup = BeautifulSoup(src, "lxml")
    all_products = soup.findAll(class_="tabel_categorie")

    products = {}
for product in all_products:
    product_text = product.text
    product_href = product.a.get("href")
    products[product_text.split()[1]] = product_href

with open("products_json.json", "w") as file:
    json.dump(products, file, indent=4, ensure_ascii=False)

with open("products_json.json") as file:
    products_json = json.load(file)

for product, href in products_json.items():
    req = requests.get(url=href, headers=headers)
    src = req.text
    with open(f"data/{product}.html", "w") as file:
        file.write(src)


for product_name in products_json:
    PRODUCT_NAME = product_name
    json_product_info = []

    with open(f"data/{PRODUCT_NAME}.html") as file:
        page = file.read()

    soup_page = BeautifulSoup(page, "lxml")
    tabel_head = soup_page.find(class_="tabelcalorii").find("tr").findAll("th")

    Aliment = tabel_head[0].text
    Calorii = tabel_head[1].text
    Proteine = tabel_head[2].text
    Lipide = tabel_head[3].text
    Carbohidrati = tabel_head[4].text
    Fibre = tabel_head[5].text
    Aproximari = tabel_head[6].text

    with open(f"csv/{PRODUCT_NAME}.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                Aliment,
                Calorii,
                Proteine,
                Lipide,
                Carbohidrati,
                Fibre,
                Aproximari
            )
        )

    tabel_rows = soup_page.find("table").find_all(class_="color0")
    tabel_rows.extend(soup_page.find("table").find_all(class_="color1"))

    for td_rows in tabel_rows:
        product_with_date = td_rows.findAll("td")

        Aliment = product_with_date[0].text
        Calorii = product_with_date[1].text
        Proteine = product_with_date[2].text
        Lipide = product_with_date[3].text
        Carbohidrati = product_with_date[4].text
        Fibre = product_with_date[5].text
        Aproximari = product_with_date[6].text

        json_product_info.append({
            "aliment": Aliment,
            "calorii": Calorii,
            "proteine": Proteine,
            "lipide": Lipide,
            "carbohidrati": Carbohidrati,
            "fibre": Fibre,
            "aproximari": Aproximari
        })
        with open(f"csv/{PRODUCT_NAME}.csv", "a", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    Aliment,
                    Calorii,
                    Proteine,
                    Lipide,
                    Carbohidrati,
                    Fibre,
                    Aproximari
                )
            )
    with open(f"json/{PRODUCT_NAME}.json", "a") as file:
        json.dump(json_product_info, file, indent=4, ensure_ascii=False)
    print(PRODUCT_NAME + " was created a json and csv file")
