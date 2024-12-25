
import time
from selenium.webdriver.common.by import By
from .baseScrapper import BaseScraper

class RealEstateScraper(BaseScraper):
    """
    A scraper specifically designed for real estate listings.
    It extends the BaseScraper and implements the unique logic/structure
    for real estate websites.
    """

    def extract_data(self, listing_url):
        """
        Extract required data from a single real estate listing.
        :param listing_url: The URL for the real estate listing to scrape.
        :return: A dictionary containing the extracted data.
        """
        self.driver.get(listing_url)
        time.sleep(5)  # Adjust sleep as necessary for page load

        data = {}

        # Extract images from slider
        try:
            images = self.driver.find_elements(By.CSS_SELECTOR, ".slick-slide img")
            data["images"] = [img.get_attribute("src") for img in images if img.get_attribute("src")]
        except Exception as e:
            print(f"Error extracting images: {e}")
            data["images"] = []

        # Extract city
        try:
            city = self.driver.find_element(By.CSS_SELECTOR, ".sc-1x0vz2r-0.iotEHk").text
            data["city"] = city if city else None
        except Exception as e:
            print(f"Error extracting city: {e}")
            data["city"] = None

        # Extract time since listing
        try:
            time_since = self.driver.find_elements(By.CSS_SELECTOR, ".sc-1x0vz2r-0.iotEHk time")
            data["time_since"] = time_since[0].text if time_since else None
        except Exception as e:
            print(f"Error extracting time since listing: {e}")
            data["time_since"] = None

        # Extract listing price
        try:
            price_element = self.driver.find_element(
                By.CSS_SELECTOR,
                ".sc-1g3sn3w-10.leGvyq p.sc-1x0vz2r-0.lnEFFR.sc-1g3sn3w-13.czygWQ"
            )
            data["price"] = price_element.text.strip() if price_element.text else None
        except Exception as e:
            print(f"Error extracting price: {e}")
            data["price"] = None

        # Extract beds, baths, and surface area
        try:
            details = self.driver.find_elements(By.CSS_SELECTOR, ".sc-6p5md9-2.bxrxrn")
            data["beds"] = details[0].text if len(details) > 0 else None
            data["baths"] = details[1].text if len(details) > 1 else None
            data["surface_area"] = details[2].text if len(details) > 2 else None
        except Exception as e:
            print(f"Error extracting details: {e}")
            data["beds"] = data["baths"] = data["surface_area"] = None

        # Extract other characteristics
        try:
            characteristics = self.driver.find_elements(By.CSS_SELECTOR, ".sc-qmn92k-1.jJjeGO")
            for char in characteristics:
                try:
                    label = char.find_element(By.TAG_NAME, "span").text
                    value = char.find_element(By.CSS_SELECTOR, ".sc-1x0vz2r-0.gSLYtF").text
                    if label and value:
                        data[label] = value
                except Exception as ce:
                    print(f"Error extracting a characteristic: {ce}")
        except Exception as e:
            print(f"Error extracting characteristics: {e}")

        # Extract description
        try:
            description = self.driver.find_element(By.CSS_SELECTOR, ".sc-ij98yj-0.fAYGMO").text
            data["description"] = description if description else None
        except Exception as e:
            print(f"Error extracting description: {e}")
            data["description"] = None

        # Extract equipment list
        try:
            equipment_elements = self.driver.find_elements(By.CSS_SELECTOR, ".sc-mnh93t-2.gONgBt")
            data["equipments"] = [equip.text for equip in equipment_elements if equip.text]
        except Exception as e:
            print(f"Error extracting equipments: {e}")
            data["equipments"] = []

        return data
