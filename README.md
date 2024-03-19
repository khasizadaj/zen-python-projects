# zen-python-projects

## Introduction

This repository is a collection of projects that were hosted by Zen Academy.


## Projects

### Web Scraping with Selenium

Project is simple example of what can be done with Selenium package. In this project, you can see these concepts:

- Accessing website through Selenium

```python
# main.py
driver.get(URL)
```

- Locating elements

```python
# main.py
driver.find_element(By.ID, "song-form")
```

- Searching inside retrieved elements

```python
# main.py
form = driver.find_element(By.ID, "song-form")
name_input = form.find_element(By.ID, "song_name-input")
```

- Waiting for element to show up

```python
# main.py
form = driver.find_element(By.ID, "song-form")
wait = WebDriverWait(driver, timeout=2)
wait.until(lambda d : form.is_displayed())
```

- Getting content of the elements

```python
# main.py

heading = song.find_element(By.CLASS_NAME, "details") \
        .find_element(By.TAG_NAME, "h3")
song_n_author = [x.strip() for x in heading.text.split("by")]
```

- Interacting with elements (clicking buttons, filling in input, submitting form (it's kinda cliking again :/) etc.)

```python
# main.py
link = driver.find_element(By.LINK_TEXT, "from here").click()

name_input = form.find_element(By.ID, "song_name-input")
name_input.send_keys(song_details["name"])
```

- Using different browsers for testing

```python
# main.py
driver = webdriver.Edge()
driver = webdriver.Chrome()
```

- Using headless browsers

```python
# main.py
options = ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)
```

> On top of these you can see how to create basic CLI (Command Line Interface) application using `argparse` package that comes with standart Python library.