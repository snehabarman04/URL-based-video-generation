from bs4 import BeautifulSoup
import requests

# Base URL for the search
URL = "https://www.amazon.in/ZEBRONICS-Connectivity-Bluetooth-Comfortable-Lightweight/dp/B0BS9KV9C1"

# Headers for request
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'
}

webpage = requests.get(URL, headers=HEADERS)
soup = BeautifulSoup(webpage.content, "html.parser")
def get_product_title(soup):
    try:
        title = soup.find("span", attrs={"id": "productTitle"}).text.strip()
    except AttributeError:
        title = "no title found"
    return title


def get_product_price(soup):
    try:
        price_symbol = soup.find("span", attrs={"class": "a-price-symbol"}).text.strip()
        price_whole = soup.find("span", attrs={"class": "a-price-whole"}).text.strip()
        price = f"{price_symbol}{price_whole}"
    except AttributeError:
        price = "no price found"
    return price


def get_about_this_item(soup):
    try:
        about_section = soup.find("div", attrs={"id": "feature-bullets"})
        about_items = [li.text.strip() for li in about_section.find_all("li")]
        about_text = "\n".join([f"{i+1}. {item}" for i, item in enumerate(about_items)])
    except AttributeError:
        about_text = ""
    return about_text


def get_customer_reviews(soup):
    try:
        reviews = soup.find("span", attrs={"class": 'a-icon-alt'}).text
    except AttributeError:
        reviews = "no review found"
    return reviews


def get_image_urls(soup):
    image_urls = []
    try:
        img_divs = soup.find_all("div", attrs={"class": "imgTagWrapper"})
        for div in img_divs:
            img_tag = div.find("img")
            if img_tag and "src" in img_tag.attrs:
                image_urls.append(img_tag["src"])
    except AttributeError:
        pass
    return image_urls



product_title = get_product_title(soup)
product_price = get_product_price(soup)
about_this_item = get_about_this_item(soup)
customer_reviews = get_customer_reviews(soup)
image_urls = get_image_urls(soup)



print(f"Product Title: {product_title}")
print(f"Product Price: {product_price}")
print("About This Item:")
print(about_this_item)
print(f"Customer Reviews: {customer_reviews}")
print("\nImage URLs:")
for idx, url in enumerate(image_urls, 1):
    print(f"{idx}. {url}")
