from selenium.webdriver.chrome.service import Service

import re
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
service = Service("C:\chromediver\chromedriver-win64\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

url = "https://www.avito.ma/fr/maroc/ventes_immobilieres-%C3%A0_vendre?cities=5,119,48,93"

def get_text_or_na(elements):
    return elements[0].text.strip() if elements else "N/A"

def get_attribute_or_na(elements, attribute):
    return elements[0].get_attribute(attribute).strip() if elements else "N/A"

listing_id_pattern = re.compile(r'_(\d+)\.htm$')

def scrape_page(driver):
    listings = driver.find_elements(By.CSS_SELECTOR, "div.sc-1nre5ec-1.crKvIr.listing > a")
    page_data = []

    for listing in listings:
        link = listing.get_attribute("href") or "N/A"
        listing_id_match = listing_id_pattern.search(link)
        listing_id = listing_id_match.group(1) if listing_id_match else "N/A"

        # Seller
        seller_name_elem = listing.find_elements(By.CSS_SELECTOR, "p.sc-1x0vz2r-0.hNCqYw")
        seller = get_text_or_na(seller_name_elem)

        # Boutique
        is_boutique = bool(listing.find_elements(By.CSS_SELECTOR, "svg[aria-labelledby='ShopBadgeTitleID']"))

        # Posted time
        posted_elem = listing.find_elements(By.CSS_SELECTOR, "div.sc-1wnmz4-3.iPMAyG p.sc-1x0vz2r-0.iFQpLP")
        posted_at = get_text_or_na(posted_elem)

        # Title
        title_elem = listing.find_elements(By.CSS_SELECTOR, "p.sc-1x0vz2r-0.iHApav")
        title = title_elem[0].get_attribute("title").strip() if title_elem else "N/A"

        # Location
        location_elem = listing.find_elements(By.CSS_SELECTOR, "p.sc-1x0vz2r-0.layWaX")
        location_text = get_text_or_na(location_elem)
        category = city = secteur = "N/A"
        if "dans" in location_text:
            parts = location_text.split("dans")
            category = parts[0].strip() if len(parts) > 0 else "N/A"
            loc_parts = parts[1].strip().split(",") if len(parts) > 1 else []
            city = loc_parts[0].strip() if len(loc_parts) > 0 else "N/A"
            secteur = loc_parts[1].strip() if len(loc_parts) > 1 else "N/A"

        # Cover image
        cover_img_elem = listing.find_elements(By.CSS_SELECTOR, "div.sc-bsm2tm-2.eDIowj img")
        cover_img = get_attribute_or_na(cover_img_elem, "src")

        # Price
        price_elem = listing.find_elements(By.CSS_SELECTOR,
                                           "div.sc-b57yxx-4.dRjnHr p.sc-1x0vz2r-0.dJAfqm.sc-b57yxx-3.IneBF")
        price = get_text_or_na(price_elem)

        # Beds, Baths, Area
        beds = baths = area = "N/A"
        param_blocks = listing.find_elements(By.CSS_SELECTOR, "div.sc-b57yxx-2.jhthcs span.sc-1s278lr-0.cAiIZZ")
        for block in param_blocks:
            div = block.find_element(By.CSS_SELECTOR, "div[title]")
            title_attr = div.get_attribute("title").strip().lower()
            block_text = div.text.strip().split()
            if "chambre" in title_attr:
                beds = block_text[0] if block_text else "N/A"
            elif "salle de bain" in title_attr:
                baths = block_text[0] if block_text else "N/A"
            elif "surface" in title_attr:
                area = " ".join(block_text) if block_text else "N/A"

        page_data.append({
            "Link": link,
            "ListingID": listing_id,
            "Category": category,
            "Seller": seller,
            "isBoutique": is_boutique,
            "PostedAt": posted_at,
            "Title": title,
            "City": city,
            "Secteur": secteur,
            "CoverImage": cover_img,
            "Price": price,
            "Beds": beds,
            "Baths": baths,
            "Area": area
        })

    return page_data

try:

    base_url = url
    all_listings = []
    page_number = 1

    while page_number < 10:
        url = f"{base_url}?o={page_number}" if page_number > 1 else base_url
        driver.get(url)
        time.sleep(5)
        page_data = scrape_page(driver)
        if not page_data:
            break
        all_listings.extend(page_data)
        page_number += 1

    with open("listings.json", "w", encoding="utf-8") as f:
        json.dump(all_listings, f, ensure_ascii=False, indent=4)
    print("Scraping complete. JSON data saved in listings.json.")

finally:
    driver.quit()


