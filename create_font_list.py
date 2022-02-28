import click
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import re
import json
import datetime

def get_themes_info():

  themes = {}

  table_div = driver.find_element(By.ID, 'menuthemes')
  theme_links = table_div.find_elements(by=By.TAG_NAME, value='a')

  # alpha_ = re.compile('\w')

  category = None

  for theme_link in theme_links:
    # print(f'cat: {theme_link.text} link: {theme_link.get_attribute("href")}')
    key = theme_link.text.strip().replace(' ', '_')
    key = re.sub('\W', '', key)
    # print(f'key: {key}')

    if re.search('bitmap.php', theme_link.get_attribute("href")):
      print(f'WARNING: skipping bitmap fonts.')
    elif re.search('mtheme', theme_link.get_attribute("href")):
      category = key
      themes[category] = {}
    elif category is not None:
      themes[category][key] = theme_link.get_attribute("href")
    else:
      print(f'WARNING: skipping {key} because no {category} is set.')

  return themes

def get_fonts(
  url,
  category,
  theme,
):
  url += '&sort=date&fpp=200'

  if free_only:
    url += '&l[]=10&l[]=1'

  driver.get(url)
  # print(url)

  # max_page_count
  noindex_div = driver.find_elements(by=By.CLASS_NAME, value='noindex')[0]
  page_links = noindex_div.find_elements(by=By.TAG_NAME, value='a')
  max_page_count = 1
  for l in page_links:
    try:
      num = int(l.text)
      max_page_count = max(max_page_count, num)
    except ValueError:
      pass

  # print(max_page_count)

  for i in range(max_page_count):
    page_num = i + 1
    page_url = url + '&page=' + str(page_num)
    # print(page_url)

    driver.get(page_url)

    all_fonts.extend(collect_font_info(category, theme))

    if debug:
      break

  # max_page_count


def collect_font_info(category, theme):
  fonts = []

  info_elements = driver.find_elements(by=By.CLASS_NAME, value='lv1left')
  download_elements = driver.find_elements(by=By.CLASS_NAME, value='dl')

  # print(len(info_elements), len(download_elements))

  assert(len(info_elements) == len(download_elements))

  for i in range(len(info_elements)):
    info_e = info_elements[i]
    download_e = download_elements[i]

    info_links = info_e.find_elements(by=By.TAG_NAME, value='a')
    if len(info_links) < 2:
      continue
    font_name = info_links[0].text
    font_link = info_links[0].get_attribute('href').split('?')[0]
    font_creator = info_links[1].text
    font_download = download_e.get_attribute('href')

    font = {
      'name': font_name,
      'dafont_link': font_link,
      'creator': font_creator,
      'download': font_download,
      'category': category,
      'theme': theme,
    }

    fonts.append(font)

    # if debug:
    #   break
  
  return fonts
  

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
@click.option(
  '--debug_run',
  is_flag=True,
  help='Run only the first element in lists to help with debugging. And will keep browser window open.',
)
@click.option(
  '--non_free',
  is_flag=True,
  help='Include non free fonts.',
)
@click.option(
  '-o',
  '--out_path',
  type=click.Path(exists=False),
  default=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cache', 'font_list.json')),
  show_default=True,
  help='Where to save the manifest.'
)
def scrape(
  no_cache,
  exe_path,
  themes_cache,
  debug_run,
  non_free,
  out_path,
):
  global driver
  global free_only
  global debug
  global all_fonts

  all_fonts = []

  use_cache = not no_cache
  free_only = not non_free
  debug = debug_run

  driver = webdriver.Chrome(executable_path=exe_path)
  driver.get("https://www.dafont.com/")
  assert "DaFont" in driver.title

  if use_cache and os.path.exists(themes_cache):
    f = open(themes_cache, 'r')
    themes = json.load(f)
  else:
    themes = get_themes_info()
    if use_cache:
      f = open(themes_cache, 'w') 
      json.dump(themes, f, indent=4) 
      f.close()

  # print(themes)

  for category in themes.keys():
    for theme in themes[category].keys():
      fonts = get_fonts(themes[category][theme], category, theme)

      if debug:
        break
    if debug:
      break

  # print(all_fonts)

  d_name = 'dafonts-'
  if free_only:
    d_name += 'free'
  else:
    d_name += 'nonfree'

  font_list = {
    'dataset_name': d_name,
    'date': str(datetime.datetime.now()),
    'font_info': all_fonts
  }

  os.makedirs(os.path.dirname(out_path), exist_ok=True)

  f = open(out_path, 'w') 
  json.dump(font_list, f, indent=4) 
  f.close()

  if debug:
    while(True):
      pass



if __name__ == '__main__':
  scrape()

