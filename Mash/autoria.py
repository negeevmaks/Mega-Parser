import asyncio
from itertools import cycle
from bs4 import BeautifulSoup
import ui
from playwright.async_api import async_playwright
import openpyxl
from Mash.cars import Cars

base_url = 'https://auto.ria.com/uk/car/'


def check_model_exists(result_file, url, ws):
    for row in ws.iter_rows(min_row=2):
        cell_value = row[0].value

        if url in cell_value:
            return True

    return False

async def process_link(link, result_file, wb, ws):
    if check_model_exists(result_file, link, ws):
        print(link)
        print('skiped')
        return None

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()

            context = await browser.new_context()
            page = await context.new_page()
            await page.goto(link)

            content = await page.content()
            soup = BeautifulSoup(content, 'html.parser')

            name = soup.find('h3', {'class': 'auto-content_title'})
            name = name.text if name else None

            locate = soup.find('div', {'class': 'item_inner'})
            locate = locate.text if locate else None

            price = soup.find('strong')

            if price:
                price_text = price.text

                if '$' in price_text:
                    price = price_text

                elif 'грн' in price_text:
                    price = price_text

                else:
                    return None

            else:
                price = None

            print(name, price, locate)

            # Extract phone number
            await page.click('.phone_show_link')
            await asyncio.sleep(1)
            number_element = await page.query_selector('.popup-successful-call-desk')
            number = await number_element.text_content() if number_element else None

            print(number)

            last_row = ws.max_row + 1

            ws[f'A{last_row}'] = f'URL: {link}'
            ws[f'B{last_row}'] = f'Model: {name}'
            ws[f'C{last_row}'] = f'Price: {price}'
            ws[f'D{last_row}'] = f'Number: {number}'
            ws[f'E{last_row}'] = f'Locate: {locate}'

            wb.save(f'{result_file}/autoria.xlsx')

            await browser.close()

    except Exception as e:
        print(f"Error processing link {link}: {str(e)}")

async def main(Ca, value, result_file, category):
    wb = openpyxl.load_workbook(f'{result_file}/autoria.xlsx')
    ws = wb.active
    
    num = 0
    links = await Ca.base_requ(value, category)

    sub_string = "check_selection"
    links = {url for url in links if sub_string not in url}

    cars_res = len(links)
    links = list(links)  # Convert set to a list

    for i in range(0, len(links)):
        link = links[i]
        tasks = [process_link(link, result_file, wb, ws)]
        await asyncio.gather(*tasks)

        num += len(link)
        ui.ui_update(cars_res, num)

async def write_link(link, cars_res, num, result_file):
    wb = openpyxl.load_workbook(f'{result_file}/autoria.xlsx')
    ws = wb.active

    await process_link(link, result_file, wb, ws)

    print(f'Writing process: {num}/{cars_res}')

    ui.ui_update(cars_res, num)

def start_parsing(value, result_file, category):
    Ca = Cars()

    def create_workbook(path):
        workbook = openpyxl.Workbook()
        workbook.save(path)

    create_workbook(f'{result_file}/autoria.xlsx')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(Ca, value, result_file, category))
