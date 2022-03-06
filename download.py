import click
import os
import json
import wget
import re
import zipfile 
from concurrent import futures
from utils import path_format

def download_font(font):
  to_download_path = os.path.join(output_path, path_format(font['category']), path_format(font['theme']), path_format(font['creator']), path_format(font['name']))
  print(to_download_path)

  if not os.path.isdir(to_download_path):
    os.makedirs(to_download_path)
    # os.chdir(to_download_path)
    zip_path = os.path.join(to_download_path, path_format(font['name'] + '.zip'))
    wget.download(font['download'], zip_path)

    if os.path.isfile(zip_path):
        with zipfile.ZipFile(zip_path) as zip:
          zip.extractall(to_download_path)

        os.remove(zip_path)
    else:
      print('WARNING {zip_path} does not exist.')


@click.command()
@click.option(
  '-i',
  '--input',
  type=click.Path(exists=True),
  help='font_list.json created by running create_font_list.py.',
  default=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cache', 'font_list.json')),
  show_default=True,
)
@click.option(
  '-o',
  '--output',
  type=click.Path(),
  help='The root directory of where fonts should be downloaded to. Will skip fonts that have already been downloaded.',
  default=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'download')),
  show_default=True,
)
def download(
  input,
  output,
):

  global output_path
  output_path = output

  f = open(input, 'r')
  data = json.load(f)

  # print(data)

  os.makedirs(output, exist_ok=True)

  ex = futures.ThreadPoolExecutor()
  ex.map(download_font, data['font_info'])
  

if __name__ == '__main__':
  download()