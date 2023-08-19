import ui
from Mash.autoria import start_parsing as autoria_start_parsing
from Mash.cars import Cars
from Mash.machinery import start_parsing as machinery_start_parsing, get_category as machinery_get_category
from Mash.autoline import start_parsing as autoline_start_parsing, get_category as autoline_get_category
from Mash.agroline import start_parsing as agroline_start_parsing, get_category as agroline_get_category

def result(result):
    site = result['site']
    category = result['options']
    price = (result['min_price'], result['max_price'])
    cars = result['amount']
    result_folder = result['folderpath']
    window = result['window']

    if site == 'AUTO.RIA':
        autoria_start_parsing(cars, result_folder, category, price)
        
    elif site == 'Machineryline':
        machinery_start_parsing(category, price, cars, result_folder)

    elif site == 'Autoline':
        autoline_start_parsing(category, price, cars, result_folder)

    elif site == 'Agriline':
        agroline_start_parsing(category, price, cars, result_folder)

def checks(value):
    if value == 'AUTO.RIA':
        car_obj = Cars()
        categories = car_obj.category()
        
        return categories

    elif value == 'Machineryline':
        return machinery_get_category()

    elif value == 'Autoline':
        return autoline_get_category()

    elif value == 'Agriline':
        return agroline_get_category()

if __name__ == '__main__':
    ui.start()
