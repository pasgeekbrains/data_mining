#from pathlib import Path
#import requests

#params = {'store':None,
#          'records_per_page':12,
#          'page':2,
#          'categories':None,
#          'ordering':None,
#          'price_promo__gte':None,
#          'price_promo__lte':None,
#          'search':None
#          }
#headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0;) Gecko/20100101 Firefox/70.0"}
#headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/70.0"}



#url = "https://5ka.ru/api/v2/special_offers/"

#response = requests.get(url, params=params, headers=headers )

#result_html_file = Path(__file__).parent.joinpath('5ka.html')
#result_json_file = Path(__file__).parent.joinpath('5ka.json')

#result_html_file.write_text(response.text, encoding='UTF-8')
#result_json_file.write_text(response.text, encoding='UTF-8')

from pathlib import Path
import requests
import time
import json

class Spider5ka:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0;) Gecko/20100101 Firefox/70.0"}
    def __init__(self, startUrl: str, saveFolder: Path):
        self.startUrl = startUrl
        self.saveFolder = saveFolder

    def _get_response(self, url):
        while True:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response
            time.sleep(0.5)

    def _spider(self, url:str):
        while url:
            response = self._get_response(url)
            data: dict = response.json()
            url = data["next"]
            for product in data["results"]:
                yield product

    def _save(self, data: dict, filePath: Path):
        filePath.write_text(json.dumps(data, ensure_ascii=False))

    def run(self):
        for product in self._spider(self.startUrl):
            productPath = self.saveFolder.joinpath(f"{product['id']}.json")
            self._save(product, productPath)


class СategoriesSpider5ka(Spider5ka):
    def __init__(self, categoriesUrl:str, *args, **kwargs):
        self.categoriesUrl = categoriesUrl
        super().__init__(*args, **kwargs)

    def run(self):
        for category in self._get_response(self.categoriesUrl).json():
            category["products"] = []
            params = f"?categories={category['parent_group_code']}"
            url = f"{self.startUrl}{params}"

            category["products"].extend(list(self._spider(url)))
            fileName = f"{category['parent_group_code']}.json"
            catPath = self.saveFolder.joinpath(fileName)
            self._save(category, catPath)




if __name__ == '__main__':
    url = "https://5ka.ru/api/v2/special_offers/"
    catUrl = "https://5ka.ru/api/v2/categories/"
#    saveFolder = Path(__file__).parent.joinpath('products')
#    if not saveFolder.exists():
#        saveFolder.mkdir(

#        )
#    spider = Spider5ka(url, saveFolder)
#    spider.run()

    saveFolder = Path(__file__).parent.joinpath('categories')
    if not saveFolder.exists():
        saveFolder.mkdir()
    cat_parser = СategoriesSpider5ka(catUrl, url, saveFolder)
    cat_parser.run()





#print(1)
