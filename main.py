import yaml
import src.scraping as scrup


with open('config.yaml', 'r') as file:
    prime_service = yaml.safe_load(file)

URL = f"https://www.list.am/en/category/56/"
MAX = prime_service['price_max']
MIN = prime_service['price_min']
LOC = prime_service['location']
pages = prime_service['page']

scrup.parse_run(URL, LOC , MIN , MAX, pages)

