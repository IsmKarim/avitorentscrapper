
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from propertiesSaleScrapper import RealEstateScraper
from rentalsScrapper import RentalScraper
import os
import json

def setup_webdriver(driver_path: str = "C:\\chromedriver\\chromedriver.exe"):
    """
    Setup and return a Selenium WebDriver instance.
    :param driver_path: Path to the chromedriver binary.
    """
    options = Options()
    # Example: uncomment if you want headless mode
    # options.add_argument("--headless")

    service = Service(driver_path)
    return webdriver.Chrome(service=service, options=options)


def load_listings(file_path: str):
    """
    Read and return the contents of a JSON file containing listings.
    """
    if not os.path.exists(file_path):
        print(f"File {file_path} not found. Returning empty list.")
        return []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            listings = json.load(file)
            return listings
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in {file_path}: {e}")
        return []


def save_results(results, file_path: str):
    """
    Save the scraping results to a JSON file.
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(results, file, ensure_ascii=False, indent=4)
        print(f"Results saved to {file_path}.")
    except Exception as e:
        print(f"Error saving results: {e}")


def main(
    category: str = "real_estate",
    listings_file: str = "data/listings.json",
    output_file: str = "results/results.json",
    driver_path: str = "C:\\chromedriver\\chromedriver.exe"
):
    """
    Main function to coordinate the scraping process.
    Allows direct invocation with arguments, rather than CLI.

    :param category: Which category scraper to use.
                     Options: "real_estate", "rentals", "electronics"
    :param listings_file: Path to the input JSON file.
    :param output_file: Path to save the scraped results.
    :param driver_path: Path to your ChromeDriver executable.
    """
    # 1. Setup the WebDriver
    driver = setup_webdriver(driver_path)

    # 2. Load the listings
    listings = load_listings(listings_file)
    if not listings:
        print("No listings found to scrape.")
        driver.quit()
        return

    # 3. Select the appropriate scraper
    if category == "real_estate":
        scraper = RealEstateScraper(driver)
    elif category == "rentals":
        scraper = RentalScraper(driver)

    else:
        print(f"Unsupported category: {category}")
        driver.quit()
        return

    # 4. Scrape
    results = scraper.scrape_listings(listings)

    # 5. Save results
    save_results(results, output_file)

    # 6. Cleanup
    driver.quit()


if __name__ == "__main__":
    # Example usage: call main with whatever defaults or values you prefer
    main(
        category="real_estate",
        listings_file="../listings.json",
        output_file="results/results.json",
        driver_path="C:\\chromedriver\\chromedriver.exe"
    )
