import argparse
from enum import Enum
import json
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver


URL = "https://happy-new-year.javidkhasizada.xyz/"


class Action(Enum):
    LIST = "list"

    def __str__(self):
        return self.value

class Browser(Enum):
    EDGE = "edge"
    CHROME = "chrome"

    def __str__(self):
        return self.value

def get_driver(browser: Browser) -> WebDriver:
    if browser == Browser.EDGE:
        return webdriver.Edge()
    elif browser == Browser.CHROME:
        return webdriver.Chrome()
    else:
        raise ValueError("Invalid browser type")


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


def main(driver: WebDriver, action: Enum, output_file: str) -> None:
    driver.get(URL)
    
    if action == Action.LIST:
        output = get_all_songs()

    with open(f"{output_file}.json", "w") as f:
        json.dump(output, f, indent=4)


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
    args = args.parse_args()

    try:
        driver = get_driver(args.browser)
    except ValueError as e:
        print(f"An error occurred: {e}")
        exit(1)

    main(driver=driver, action=args.action, output_file=args.output)
    driver.close()
    exit(0)
