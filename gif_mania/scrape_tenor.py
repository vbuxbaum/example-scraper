import os

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By


def find_gifs(browser: webdriver.Firefox):
    figs = browser.find_elements(By.CLASS_NAME, "GifListItem")
    gifs = {}
    for fig in figs:
        try:
            idx = fig.get_attribute("data-index")
            url = fig.find_element(By.TAG_NAME, "img").get_attribute("src")
            gifs[idx] = url
        except Exception:
            pass
    return gifs


def save_gif(idx: int, url: str):
    if not os.path.isdir("tenor"):
        os.mkdir("tenor")

    with open(f"./tenor/{idx}.gif", "wb") as file:
        res = requests.get(url, stream=True)
        for block in res.iter_content(1024):
            if not block:
                break
            file.write(block)


def save_multiple_gifs(previously_saved: list, found_gifs: dict):
    for idx, url in found_gifs.items():
        if idx not in previously_saved:
            save_gif(idx, url)
            previously_saved.append(idx)


def main(browser: webdriver.Firefox):
    browser.get("https://tenor.com")

    saved = []
    while True:
        found_gifs = find_gifs(browser)

        if not found_gifs:
            continue

        save_multiple_gifs(saved, found_gifs)

        browser.execute_script("window.scrollBy(0, 250)")


if __name__ == "__main__":

    with webdriver.Firefox() as browser:
        input("Aperte ENTER para iniciar a busca!")
        main(browser)
