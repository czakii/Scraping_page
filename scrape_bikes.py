from bs4 import BeautifulSoup
import requests
import json

def scrape_product_detail_page(product_detail_url):
    source = requests.get(product_detail_url)
    if source.status_code != 200:
        print('Can not connect to url')
        return dict()

    soup = BeautifulSoup(source.content, 'html.parser')
    body = soup.body

    bike_dict = dict.fromkeys(['model','url','main_photo_path','additional_photo_paths','price','model_year','parameters'])
    bike_dict['parameters'] = dict.fromkeys(['weight','frame'])
    bike_dict['url'] = product_detail_url

    #model and photo
    detail_page = body.find('div', id='detail_page')
    if detail_page:
        detail_page_center = detail_page.find('div',class_='center')
        if detail_page_center:
            model = detail_page_center.find('h1')
            if model:
                bike_dict['model'] = model.text
            
            main_photo_path = detail_page_center.find('img')
            if main_photo_path:
                if 'https' not in main_photo_path['src']:
                    bike_dict['main_photo_path'] = 'https://www.lapierre-bike.cz' + main_photo_path['src']
                else:
                    bike_dict['main_photo_path'] = main_photo_path['src']
            
    #additional photos
    additional_photo_paths_list = body.find('div', class_='pohledy')
    if additional_photo_paths_list:
        additional_photo_paths = []
        all_photos = additional_photo_paths_list.find_all('a')
        if all_photos:
            for photo in all_photos:
                photo_path = photo.find('img')
                if photo_path:
                    additional_photo_paths.append(photo_path['src'])
            bike_dict['additional_photo_paths'] = additional_photo_paths

    #price
    price_div = body.find('div', class_='cena')
    if price_div:
        bike_dict['price'] = int(price_div.span.text.removesuffix('CZK').replace('.','').replace(' ',''))

    #bike specifications
    for specifications in body.find_all('table', class_='spec'):
        for spec in specifications.find_all('tr'):
            if spec.find_all('td')[1].text == 'Ročník':
                bike_dict['model_year'] = int(spec.find_all('td')[2].text)
            if spec.find_all('td')[1].text == 'Hmotnost':
                bike_dict['parameters']['weight'] = spec.find_all('td')[2].text
            if spec.find_all('td')[1].text == 'Rám':
                bike_dict['parameters']['frame'] = spec.find_all('td')[2].text

    return bike_dict


def save_five_to_json():
    data_to_json = []
    data_to_json.append( scrape_product_detail_page('https://www.lapierre-bike.cz/produkt/spicy-cf-69/5943') )
    data_to_json.append( scrape_product_detail_page('https://www.lapierre-bike.cz/produkt/overvolt-glp-team-b500/5957') )
    data_to_json.append( scrape_product_detail_page('https://www.lapierre-bike.cz/produkt/lapierre-ezesty-am-ltd-ultimate/5951') )
    data_to_json.append( scrape_product_detail_page('https://www.lapierre-bike.cz/produkt/trekking-20-w/6019') )
    data_to_json.append( scrape_product_detail_page('https://www.lapierre-bike.cz/produkt/urban-40/5991') )


    with open('top-5-bikes.json', 'w') as json_file:
        json.dump(data_to_json, json_file)


if __name__ == "__main__":
    save_five_to_json()

