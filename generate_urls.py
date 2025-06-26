import os
from dotenv import load_dotenv
from generate_dates import get_weekend_dates

# Load API key from .env file
load_dotenv()
SCRAPER_API_KEY = os.getenv("SCRAPER_API_KEY")

def wrap_with_scraperapi(url):
    return f"http://api.scraperapi.com?api_key={SCRAPER_API_KEY}&url={url}"

def generate_skyscanner_urls(origin, destinations, num_weeks=4):
    weekends = get_weekend_dates(num_weeks)
    urls = []

    for destination in destinations:
        for depart, return_ in weekends:
            base_url = f"https://www.skyscanner.ca/transport/flights/{origin}/{destination}/{depart}/{return_}"
            proxied_url = wrap_with_scraperapi(base_url)
            urls.append(proxied_url)

    return urls

# Optional test run
if __name__ == "__main__":
    test_origin = "YUL"
    test_destinations = ["YYZ", "JFK"]
    generated_urls = generate_skyscanner_urls(test_origin, test_destinations, num_weeks=2)
    
    for url in generated_urls:
        print(url)
