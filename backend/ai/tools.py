import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from utility.selenium import get_driver, get_element
from langchain.document_loaders import ImageCaptionLoader, SeleniumURLLoader
import pytesseract, requests

load_dotenv()
if os.environ.get('DEBUG_MODE') == 'True':
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def search_flipkart(query: str) -> str:
    """Search Flipkart for available clothes/accessories for the given query"""
    driver = get_driver()
    url = f"https://www.flipkart.com/search?q={query}"
    driver.get(url)
    products = f"Available product for \"{query}\" are:\n"
    product_rows = get_element(driver, By.CLASS_NAME, '_13oc-S', many=True)
    i = 1
    for row in product_rows:
        soup = BeautifulSoup(row.get_attribute("innerHTML"), features="html.parser")
        for product in soup.find_all('div', recursive=False):
            link = product.find('a').attrs['href']
            id = link.split('?')[0].split('/')[-1]
            title = product.find('a', {'class': 's1Q9rs'}).attrs['title']
            try:
                price = product.find('div', {'class': '_30jeq3'}).text
            except:
                price = "Not available"
            link = link.split('&')[0]
            image = product.find('img').attrs['src']
            products += f"{i}. {title} (Product ID: {id}) | Price: {price} | Image URL: {image} | Product URL: https://www.flipkart.com{link}\n"
            i += 1
    return products


def generate_image_caption(image_url: str) -> str:
    """Generate caption for the given image url"""
    response = requests.get(image_url)
    if response.status_code == 200:
        with open("./temp.jpeg", 'wb') as f:
            f.write(response.content)
    loader = ImageCaptionLoader(path_images=['./temp.jpeg'])
    data = loader.load()
    caption = data[0].dict()['page_content']
    os.remove('./temp.jpeg')
    return caption
