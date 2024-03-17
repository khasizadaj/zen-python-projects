import argparse
from enum import Enum
import json
from pprint import pprint
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver import ChromeOptions
from selenium.webdriver import EdgeOptions

URL = "https://happy-new-year.javidkhasizada.xyz/"


class Action(Enum):
    LIST = "list"
    ADD = "add"

    def __str__(self):
        return self.value

class Browser(Enum):
    EDGE = "edge"
    CHROME = "chrome"

    def __str__(self):
        return self.value

def get_driver(browser: Browser, headless: bool = True) -> WebDriver:

    if browser == Browser.EDGE:
        # TODO refactor further
        if (headless):
            options = EdgeOptions()
            options.add_argument("--headless=new")
            driver = webdriver.Edge(options=options)
        else:
            driver = webdriver.Edge()
    elif browser == Browser.CHROME:
        if (headless):
            options = ChromeOptions()
            options.add_argument("--headless=new")
            driver = webdriver.Chrome(options=options)
        else:
            driver = webdriver.Chrome()
    else:
        raise ValueError("Invalid browser type")
    
    driver.implicitly_wait(2)
    return driver


def get_song_details(song: WebElement) -> dict:
    heading = song.find_element(By.CLASS_NAME, "details") \
            .find_element(By.TAG_NAME, "h3")
    song_n_author = [x.strip() for x in heading.text.split("by")]

    url = song.find_element(By.CLASS_NAME, "actions") \
            .find_element(By.TAG_NAME, "a").get_attribute("href")

    return {
        "name" : song_n_author[0].replace("\"", ""),
        "author" : song_n_author[1],
        "url" : url,
    }


def get_all_songs() -> dict:
    output = []

    try:
        results = driver.find_elements(By.CLASS_NAME, "song")
        for result in results:
            output.append(get_song_details(result))
        return output
        
    except Exception as e:
        print(f"An error occurred: {e}")


def add_song(song_details: dict) -> None:
    link = driver.find_element(By.LINK_TEXT, "from here")

    # scroll to the element to be able to click it
    ActionChains(driver)\
        .scroll_to_element(link)\
        .perform()
    link.click()

    form = driver.find_element(By.ID, "song-form")

    wait = WebDriverWait(driver, timeout=2)
    wait.until(lambda d : form.is_displayed())
    
    name_input = form.find_element(By.ID, "song_name-input")
    name_input.send_keys(song_details["name"])

    artist_input = form.find_element(By.ID, "song_artist-input")
    artist_input.send_keys(song_details["author"])

    link_input = form.find_element(By.ID, "song_link-input")
    link_input.send_keys(song_details["url"])

    submit = driver.find_element(By.XPATH, '//*[@id="song-form"]/button[1]')
    submit.click()

    output = {
        "status": "success",
        "message": "Song added successfully"
    }
    return output


def main(driver: WebDriver, action: Enum, output_file: str) -> None:
    driver.get(URL)
    
    if action == Action.LIST:
        output = get_all_songs()
    elif action == Action.ADD:
        song_details = {
            "name": "Space Song",
            "author": "Beach House",
            "url": "https://music.youtube.com/watch?v=uSDWUx7S8dw",
        }
        output = add_song(song_details=song_details)
        


    with open(f"{output_file}.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4)


def str_to_bool(s: str) -> bool:
    return s.lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']


if __name__ == "__main__":
    args = argparse.ArgumentParser(description="Scrape the Happy New Year website")

    args.add_argument(
        "--action", "-a",
        type=Action,
        choices=list(Action),
        default=Action.LIST,
        help="The action to perform"
    )
    args.add_argument(
        "--browser", "-b",
        type=Browser,
        choices=list(Browser),
        default=Browser.EDGE,
        help="The browser to use for scraping"
    )
    args.add_argument(
        "--output", "-o",
        type=str,
        default="output",
        help="The output file")
    args.add_argument(
        "--debug", "-d",
        type=str_to_bool,
        default=False,
        help="The output file")
    args = args.parse_args()


    try:
        driver = get_driver(args.browser, headless=not args.debug)
    except ValueError as e:
        print(f"An error occurred: {e}")
        exit(1)

    main(driver=driver, action=args.action, output_file=args.output)
    driver.close()
    exit(0)
