import ui
import Mash.autoria
from Mash.cars import Cars
import Mash.machinery
import Mash.autoline
import Mash.agroline

def result(result):
    site = result['site']
    category = result['options']
    price = (result['min_price'], result['max_price'])
    cares = result['amount']
    result_folder = result['folderpath']
    window = result['window']

    if site == 'AUTO.RIA':
        Mash.autoria.start_parsing(cares, result_folder, category)

    elif site == 'Machineryline':
        Mash.machinery.start_parsing(category, price, cares, result_folder)

    elif site == 'Autoline':
        Mash.autoline.start_parsing(category, price, cares, result_folder)

    elif site == 'Agriline':
        Mash.agroline.start_parsing(category, price, cares, result_folder)

def checks(value):
    if value == 'AUTO.RIA':
        Ca = Cars()

        chan = Ca.category()
        return chan

    elif value == 'Machineryline':
        return Mash.machinery.get_category()

    elif value == 'Autoline':
        return Mash.autoline.get_category()

    elif value == 'Agriline':
        return Mash.agroline.get_category()

if __name__ == '__main__':
    ui.start()
