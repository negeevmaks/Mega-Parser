from requests_html import AsyncHTMLSession
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
import requests

class Cars:
    def __init__(self):
        self.base_url = 'https://auto.ria.com/uk/newauto/catalog/'
        self.session = AsyncHTMLSession()

    async def run(self):
        response = await self.session.get(self.base_url)
        self.soup = BeautifulSoup(response.text, 'html.parser')

    def category(self):
        response = requests.get(self.base_url)
        self.soup = BeautifulSoup(response.text, 'html.parser')

        brends = []
        add = []
        new = []

        ads = self.soup.find_all('section', {'class': 'box-panel line'})

        for ad in ads:
            add += ad.find_all('div', {'class': 'catalog-brands'})

        for ad in ads:
            brends += ad.find_all('a')

            for brand in brends:
                link = brand.get('href')
                new.append(link.replace('/uk/newauto/catalog/', '').replace('/', ''))

            new = list(set(new))

        return new

    async def base_requ(self, value, category):
        print(category)
        lane = []

        for link in category:
            links = self.linkas(link)

            for lin in links:
                lane.append(lin)

        lin = set()
        print(value)

        for car in lane:
            car_links = await self.get_links(car)

            print(car_links)
            print(len(car_links))
            lin.update(car_links)

            if len(lin) >= value:
                lin = set(list(lin)[:value])

                print(lin)
                print(len(lin))

                return lin

        print(lin)
        print(len(lin))

        return lin

    def linkas(self, link):
        links = set()

        response = requests.get(f'https://auto.ria.com/uk/car/{link}/?page=3')
        soup = BeautifulSoup(response.text, 'html.parser')

        num = soup.find('span', {'class': 'page-item dhide text-c'}).text

        num = num[4:]
        num = num.replace(' ', '')
        num = int(num)

        modified_link = link.replace('/uk/newauto/catalog/', '').replace('/', '')
        links.add(modified_link)
        print(num)

        for page in range(2, num+1):
            modified_link = link.replace('/uk/newauto/catalog/', '').replace('/', '') + f'/?page={page}'
            links.add(modified_link)

        return links

    async def get_links(self, url):
        base_url = 'https://auto.ria.com/uk/car/'
        full_url = base_url + url

        async with async_playwright() as p:
            browser = await p.chromium.launch()
            print(full_url)

            context = await browser.new_context()
            page = await context.new_page()

            await page.goto(full_url, timeout=0)

            url = []

            content = await page.content()

            soup = BeautifulSoup(content, 'html.parser')

            addresses = soup.find_all('a', {'class': 'address'})
            temp = soup.find_all('a', {'class': 'blue'})

            for templ in temp:
                addresses.append(templ)

            print('Len: ', len(addresses))

            for address in addresses:
                print('go')

                url.append(address.get('href'))

            await browser.close()
            return url
