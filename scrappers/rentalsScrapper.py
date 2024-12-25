

import time
from selenium.webdriver.common.by import By
from .baseScrapper import BaseScraper

class RentalScraper(BaseScraper):
    def extract_data(self, listing_url):
        """
        Extract required data from a single rental listing.
        :param listing_url: The URL for the rental listing to scrape.
        :return: A dictionary containing the extracted data.
        """
        self.driver.get(listing_url)
        time.sleep(5)  # Adjust sleep as necessary for page load

        data = {}

        # Example: Extract images
        try:
            images = self.driver.find_elements(By.CSS_SELECTOR, ".rental-slide img")
            data["images"] = [img.get_attribute("src") for img in images if img.get_attribute("src")]
        except Exception as e:
            print(f"Error extracting images: {e}")
            data["images"] = []

        # Example: Extract city
        try:
            city = self.driver.find_element(By.CSS_SELECTOR, ".rental-city span").text
            data["city"] = city if city else None
        except Exception as e:
            print(f"Error extracting city: {e}")
            data["city"] = None

        # Example: Extract monthly rent
        try:
            rent_element = self.driver.find_element(By.CSS_SELECTOR, ".rental-price")
            data["rent"] = rent_element.text.strip() if rent_element.text else None
        except Exception as e:
            print(f"Error extracting monthly rent: {e}")
            data["rent"] = None

        # Example: Extract property type
        try:
            property_type_element = self.driver.find_element(By.CSS_SELECTOR, ".rental-type")
            data["property_type"] = property_type_element.text.strip() if property_type_element.text else None
        except Exception as e:
            print(f"Error extracting property type: {e}")
            data["property_type"] = None

        # Example: Extract details like number of rooms, surface area, etc.
        try:
            details = self.driver.find_elements(By.CSS_SELECTOR, ".rental-details span")
            data["rooms"] = details[0].text if len(details) > 0 else None
            data["surface_area"] = details[1].text if len(details) > 1 else None
        except Exception as e:
            print(f"Error extracting rental details: {e}")
            data["rooms"] = data["surface_area"] = None

        # Example: Extract description
        try:
            description_element = self.driver.find_element(By.CSS_SELECTOR, ".rental-description")
            data["description"] = description_element.text if description_element.text else None
        except Exception as e:
            print(f"Error extracting description: {e}")
            data["description"] = None

        # Add more fields as necessary for rentals

        return data
