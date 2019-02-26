import json
import time
from os.path import dirname, realpath, join

from selenium import webdriver


class Parser():
    def __init__(self):
        path = join(dirname(realpath(__file__)), "chromedriver.exe")
        print(path)
        self.driver = webdriver.Chrome(executable_path=path)

    def get_info(self, tea, information):
        self.driver.get(information)
        time.sleep(1)

        try:
            info = self.driver.find_element_by_class_name("article-w").text
        except:
            print("I cannot find text")
            return None

        result = ''
        return result

    def parse(self, page):
        self.driver.get("http://teahaven.ru/wiki/page/" + str(page))
        base_teas = dict()
        teas_info = self.driver.find_element_by_class_name("feed-lst").find_elements_by_class_name("feed-item")
        for tea_info in teas_info:
            url = tea_info.get_attribute('href')
            name = tea_info.text
            base_teas[name] = str(url)

        print(f"found {len(base_teas)} teas: {base_teas}")

        full_teas = []
        for tea in base_teas:
            info = self.get_info(tea, base_teas[tea])
            if info is not None:
                full_teas.append({"name": tea, "link": base_teas[tea], "info": info})
        return full_teas


if __name__ == "__main__":
    parser = Parser()
    teas = []
    for i in range(4):
        teas.append(parser.parse(page=i + 1))
    with open(f'output.json', 'w', encoding="utf-8") as file:
        json.dump(teas, file, ensure_ascii=False)
