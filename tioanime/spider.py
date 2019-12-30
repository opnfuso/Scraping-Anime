# Importar librerias y funciones
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
import json


def writeToJSONFile(path, fileName, data):
    filePathNameWExt = './' + path + '/' + fileName + '.json'
    with open(filePathNameWExt, 'w') as fp:
        json.dump(data, fp)


# Abrir el navegador y configurarlo
options = webdriver.ChromeOptions()
# options.add_argument("--headless")
# options.add_argument(
#     "--enable-features=SameSiteByDefaultCookies,CookiesWithoutSameSiteMustBeSecure")
options.add_argument("--incognito")
driver = webdriver.Chrome(executable_path="../chromedriver", options=options)
url = "https://tioanime.com/directorio"
driver.get(url)

last_page = driver.find_element_by_xpath(
    "//*[@id='tioanime']/div/div/aside[1]/nav/ul/li[9]/a").text

last_page = int(last_page)

for i in range(1, last_page):
    url = driver.current_url
    # Contar los animes de la primera pagina pagina
    animes = driver.find_elements_by_xpath("//article/a")

    anime_info = []

    for i in range(0, len(animes)):
        animes = driver.find_elements_by_xpath("//article/a")
        animes[i].click()
        title = driver.find_element_by_xpath("//h1").text
        categorias = driver.find_elements_by_xpath("//p/span/a")
        categories = []
        for categoria in categorias:
            text = categoria.text
            categories.append(text)

        synopsis = driver.find_element_by_xpath("//p[@class='sinopsis']").text

        url_anime = (driver.current_url)

        caps_info = []
        caps = driver.find_elements_by_xpath(
            "//ul[@class='episodes-list list-unstyled']/li/a")

        for j in range(0, len(caps)):
            caps = driver.find_elements_by_xpath(
                "//ul[@class='episodes-list list-unstyled']/li/a")
            caps[j].click()
            time.sleep(1)

            episode_title = driver.find_element_by_xpath("//h1").text
            links = []
            links_options = driver.find_elements_by_xpath(
                "//*[@id='episode-options']/li/a")

            for k in range(0, len(links_options)):
                link_title = links_options[k].get_attribute(
                    "data-original-title")
                links_options[k].click()
                iframe = driver.find_element_by_xpath(
                    "//div[@class='video']/iframe").get_attribute("src")
                dict_link = {link_title: iframe}
                links.append(dict_link)

            dict_episodes = {episode_title: links}
            caps_info.append(dict_episodes)
            driver.get(url_anime)

        dict_anime_info = {"Title": title,
                           "Categories": categories, "Synopsis": synopsis, "Episodes": caps_info}
        # print(dict_anime_info)

        writeToJSONFile('./JSON', title, dict_anime_info)

        anime_info.append(dict_anime_info)

        driver.get(url)
    next_page = driver.find_element_by_xpath(
        "//*[@id='tioanime']/div/div/aside[1]/nav/ul/li/a[contains(text(), '»')]")

    next_page.click()
writeToJSONFile('./JSON', 'TioAnime', anime_info)
print(anime_info)
driver.quit()
