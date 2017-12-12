from crawler_data import crawl_data
from db_helper import init
from export_data import export_data
from import_stations import import_stations

if __name__ == "__main__":
    print('Creating tables...')

    init()
    print('Ready!')
    print('Importing... stations')
    import_stations()
    print("Ready!")
    print("Crawling Data...")
    crawl_data()
    print('Exporting Data ...')
    export_data()
    print("Ready!")



