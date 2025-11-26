from playwright.sync_api import sync_playwright
import time
import random
import pandas as pd


def get_page(url, how_many):

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)
        page = browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080}
        )

        page.evaluate("""
            () => { 
                Object.defineProperty(navigator, 'webdriver', { get: () => false }) 
            }
        """)

        page.goto(f"{url}")

        get_url(page, how_many)

        browser.close()  

def get_url(page, how_many):

    url_list = []
    seen = set()

    url = page.locator("a.name.browsinglink.js-box-link")

    while len(url_list) < how_many:

        for i in range(url.count()):
            link = url.nth(i).get_attribute('href')
            full_url = "https://www.alza.cz" + link

            if full_url not in seen:
                url_list.append(full_url)
                seen.add(full_url)

        print("Počet unikátních odkazů:", len(url_list))

        if len(url_list) >= how_many:
            break

        page.locator("a.js-button-more.button-more.btnx.normal").click()
        page.wait_for_timeout(1200)  # drobná pauza, ať má čas načíst

    print(url_list)
    open_link(page, url_list)


def open_link(page, url_list):

    list_of_notebooks = []
    for url in url_list:
        print(f"Načítám: {url}")
        page.goto(url)
        scraper(page, url, list_of_notebooks)
        page.wait_for_timeout(random.uniform(1000, 3000))
    
    to_csv(list_of_notebooks)

def scraper(page, url, list_of_notebooks):

    # TITLE
    name = page.get_by_role("heading", level=1).inner_text()

    # PRICE
    price = page.get_by_text(",-").nth(8).inner_text().replace(",-", "").replace(" ", "")

    # HODNOCENI
    rating_element = page.locator("span.ratingValue")

    if rating_element.count() == 0:
        rating = "-"
        rating_count = "-"
    else:
        rating = float(rating_element.inner_text().replace(",", "."))
        rating_count = int(page.locator("span.ratingCount").inner_text().replace(" hodnocení", ""))

    # DOSTUPNOST
    availability = page.locator('button[data-testid="productDetail-availability-availabilityText avlType0"]').inner_text()

    # URL OBRAZKU
    image_url = page.locator("img.detailGallery-alz-21.detailGallery-alz-16.swiper-zoom-targetfalse").nth(1).get_attribute('src')

    # URL NOTEBOOK
    notebook_url = url

    # ID
    id = url.split("-")[-1].replace(".htm", "")

# PARAMETRY

    # RAM
    ram = page.locator('div[data-parameter-name="Velikost operační paměti RAM"]').first.inner_text().replace("Velikost operační paměti RAM", "").replace(" GB", "").replace(" ", "")

    # STORAGE
    storage = page.locator('div[data-parameter-name="SSD Kapacita"]').first.inner_text().replace("SSD Kapacita ", "")

    # CPU
    cpu = page.locator('div[data-parameter-name="Modelové označení procesoru"]').first.inner_text().replace("Modelové označení procesoru ", "")

    # ADDING THINKS TO LIST
    print_it(name, price, rating, rating_count, availability, image_url, notebook_url, id, ram, storage, cpu)
    to_list(list_of_notebooks, name, price, rating, rating_count, availability, image_url, notebook_url, id, ram, storage, cpu)

def to_list(list_of_notebooks, name, price, rating, rating_count, availability, image_url, notebook_url, id, ram, storage, cpu):

    list_of_notebooks.append({
        "Name": name,
        "Price": price,
        "Rating": rating,
        "Number of rating": rating_count,
        "Availability": availability,
        "Image URL": image_url,
        "Notebook URL": notebook_url,
        "ID": id,
        "RAM": ram,
        "Storage": storage,
        "CPU": cpu
    })

def print_it(name, price, rating, rating_count, availability, image_url, notebook_url, id, ram, storage, cpu):
    print(name)
    print("Price:", price)
    print("Rating:", rating)
    print("Number of Rating:", rating_count)
    print("Availability:", availability)
    print("Image URL:", image_url)
    print("Notebook URL:", notebook_url)
    print("ID:", id)
    print("RAM:", ram)
    print("Storage:", storage)
    print("CPU:", cpu)
    print("-" * 40)

def to_csv(list_of_notebooks):

    df = pd.DataFrame(list_of_notebooks)
    df.to_csv("notebooks.csv", index=False, encoding="utf-8-sig")

url = "https://www.alza.cz/notebooky/18842920.htm"
how_many = 20

get_page(url, how_many)
