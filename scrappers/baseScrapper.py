
class BaseScraper:
    """
    A base class outlining the interface for any category-specific scraper.
    """

    def __init__(self, driver):
        """
        :param driver: A Selenium WebDriver instance.
        """
        self.driver = driver

    def extract_data(self, listing_url):
        """
        Extract data from a single listing URL.
        This should be overridden by subclass scrapers.

        :param listing_url: URL of the listing to scrape.
        :return: A dictionary containing the extracted data.
        """
        raise NotImplementedError("Subclasses must implement extract_data()")

    def scrape_listings(self, listings):
        """
        Scrape data for each listing in the provided list.

        :param listings: A list of listing dictionaries (with at least a 'Link' key).
        :return: A list of result dictionaries with scraped data.
        """
        results = []
        for listing in listings:
            url = listing.get("Link", "")
            print(f"Processing listing: {url}")
            try:
                data = self.extract_data(url)
                print(data)
                results.append(data)
            except Exception as e:
                print(f"Error scraping {url}: {e}")
        return results
