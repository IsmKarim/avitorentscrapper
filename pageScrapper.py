from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json
import time


def setup_webdriver():
    """Setup and return a Selenium WebDriver instance."""
    options = Options()
    service = Service("C:\\chromediver\\chromedriver-win64\\chromedriver.exe")
    return webdriver.Chrome(service=service, options=options)

def read_listings(file_path):
    """Read and return the contents of the JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            listings = json.load(file)
            print("Listings loaded successfully:")
            return listings
    except FileNotFoundError:
        print(f"The file {file_path} was not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the file {file_path}.")
        return []
    except UnicodeDecodeError as e:
        print(f"Encoding error: {e}")
        return []

def extract_data(driver, listing_url):
    """Extract required data from a single listing."""
    driver.get(listing_url)
    time.sleep(5)

    data = {}

    try:
        # Extract images from slider
        images = driver.find_elements(By.CSS_SELECTOR, ".slick-slide img")
        data["images"] = [img.get_attribute("src") for img in images if img.get_attribute("src")]
    except Exception as e:
        print(f"Error extracting images: {e}")
        data["images"] = []

    try:
        # Extract city
        city = driver.find_element(By.CSS_SELECTOR, ".sc-1x0vz2r-0.iotEHk").text
        data["city"] = city if city else None
    except Exception as e:
        print(f"Error extracting city: {e}")
        data["city"] = None

    try:
        # Extract time since listing
        time_since = driver.find_elements(By.CSS_SELECTOR, ".sc-1x0vz2r-0.iotEHk time")
        data["time_since"] = time_since[0].text if time_since else None
    except Exception as e:
        print(f"Error extracting time since listing: {e}")
        data["time_since"] = None

    try:
        # Extract listing price from the specified tag
        price_element = driver.find_element(
            By.CSS_SELECTOR,
            ".sc-1g3sn3w-10.leGvyq p.sc-1x0vz2r-0.lnEFFR.sc-1g3sn3w-13.czygWQ"
        )
        data["price"] = price_element.text.strip() if price_element.text else None
    except Exception as e:
        print(f"Error extracting listing price: {e}")
        data["price"] = None

    try:
        # Extract beds, baths, and surface area
        details = driver.find_elements(By.CSS_SELECTOR, ".sc-6p5md9-2.bxrxrn")
        data["beds"] = details[0].text if len(details) > 0 else None
        data["baths"] = details[1].text if len(details) > 1 else None
        data["surface_area"] = details[2].text if len(details) > 2 else None
    except Exception as e:
        print(f"Error extracting beds, baths, and surface area: {e}")
        data["beds"] = data["baths"] = data["surface_area"] = None

    try:
        # Extract Type, Secteur, Salons, Surface Habitable, Age Du Bien, Etage
        characteristics = driver.find_elements(By.CSS_SELECTOR, ".sc-qmn92k-1.jJjeGO")
        for char in characteristics:
            try:
                label = char.find_element(By.TAG_NAME, "span").text
                value = char.find_element(By.CSS_SELECTOR, ".sc-1x0vz2r-0.gSLYtF").text
                if label and value:
                    data[label] = value
            except Exception as e:
                print(f"Error extracting a characteristic: {e}")
    except Exception as e:
        print(f"Error extracting characteristics: {e}")

    try:
        # Extract description
        description = driver.find_element(By.CSS_SELECTOR, ".sc-ij98yj-0.fAYGMO").text
        data["description"] = description if description else None
    except Exception as e:
        print(f"Error extracting description: {e}")
        data["description"] = None

    try:
        # Extract equipment list
        equipment_elements = driver.find_elements(By.CSS_SELECTOR, ".sc-mnh93t-2.gONgBt")
        data["equipments"] = [equip.text for equip in equipment_elements if equip.text]
    except Exception as e:
        print(f"Error extracting equipments: {e}")
        data["equipments"] = []

    return data

def scrape_listings(driver, listings):
    """Scrape data for each listing in the provided list."""
    results = []
    for listing in listings:
        print(f"Processing listing: {listing.get('Link', '')}")
        scraped_data = extract_data(driver, listing.get("Link", ""))
        combined_data = {**listing, **scraped_data}
        print(combined_data)
        results.append(combined_data)
    return results

def save_results(results, file_path):
    """Save the scraping results to a JSON file."""
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(results, file, ensure_ascii=False, indent=4)
            print(f"Results saved to {file_path}.")
    except Exception as e:
        print(f"Error saving results: {e}")

def main():
    listings_file = 'listings.json'
    results_file = 'results.json'

    # Step 1: Setup WebDriver
    driver = setup_webdriver()

    # Step 2: Read listings
    listings = read_listings(listings_file)

    # Step 3: Scrape listings
    results = scrape_listings(driver, listings)

    # Step 4: Save results
    save_results(results, results_file)

    # Cleanup
    driver.quit()

if __name__ == "__main__":
    main()
