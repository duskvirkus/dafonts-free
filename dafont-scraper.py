import click
from selenium import webdriver
import os
import re
import json

def get_themes_info(
  driver,
):

  themes = {}

  table_div = driver.find_element_by_id("menuthemes")
  theme_links = table_div.find_elements_by_tag_name("a")

  # alpha_ = re.compile('\w')

  category = None

  for theme_link in theme_links:
    print(f'cat: {theme_link.text} link: {theme_link.get_attribute("href")}')
    key = theme_link.text.strip().replace(' ', '_')
    key = re.sub('\W', '', key)
    print(f'key: {key}')

    if re.search('mtheme', theme_link.get_attribute("href")):
      category = key
      themes[category] = {}
    elif category is not None:
      themes[category][key] = theme_link.get_attribute("href")
    else:
      print(f'WARNING: skipping {key} because no {category} is set.')

  return themes

@click.command()
@click.option(
  '--no_cache',
  is_flag=True,
)
@click.option(
  '--exe_path',
  type=click.Path(exists=True),
  default=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chromedriver', 'chromedriver')),
  show_default=True,
  help='Path to chrome driver. Can be downloaded from: https://sites.google.com/chromium.org/driver/ not included in repository.'
)
@click.option(
  '--themes_cache',
  type=click.Path(),
  default=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cache', 'themes.json')),
  show_default=True,
  help='Path to themes json cache. If does not exist one will be saved at the specified location unless --no_cache is passed.'
)
def scrape(
  no_cache,
  exe_path,
  themes_cache,
):
  use_cache = not no_cache

  driver = webdriver.Chrome(executable_path=exe_path)
  driver.get("https://www.dafont.com/")
  assert "DaFont" in driver.title

  if use_cache and os.path.exists(themes_cache):
    f = open(themes_cache, 'r')
    themes = json.load(f)
  else:
    themes = get_themes_info(driver)
    if use_cache:
      f = open(themes_cache, 'w') 
      json.dump(themes, f) 
      f.close()

  print(themes)

  while(True):
    pass



if __name__ == '__main__':
  scrape()

