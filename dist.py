import click
import os
import shutil
import json

from utils import path_format

@click.command()
@click.option(
  '-o',
  '--output',
  type=click.Path(exists=False),
  help='The root directory for dist.',
  default=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dist')),
  show_default=True,
)
@click.option(
  '-i',
  '--input',
  type=click.Path(exists=True),
  help='font_list.json created by running create_font_list.py.',
  default=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cache', 'font_list.json')),
  show_default=True,
)
@click.option(
  '--downloads_path',
  type=click.Path(exists=True),
  help='Download director created by running download.py.',
  default=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'download')),
  show_default=True,
)
@click.option(
  '--print_extension_info',
  is_flag=True,
  help='Will print sorted dictionary of extensions and exit.',
)
def dist(
  output,
  input,
  downloads_path,
  print_extension_info,
):
  project_root = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))

  os.makedirs(output)
  fonts_output = os.path.join(output, 'fonts')
  os.makedirs(fonts_output)

  shutil.copyfile(os.path.join(project_root, 'LICENCE.md'), os.path.join(output, 'LICENCE.md'))

  csv_file = open(os.path.join(output, 'info.csv'), 'w')

  csv_file.write('filename,base_font_name,file_format,creator,category,theme')

  f = open(input, 'r')
  data = json.load(f)

  if print_extension_info:
    extensions = {}

  num_fonts = []
  all_font_creators = []
  date_scraped = data['date']
  
  for font in data['font_info']:
    downloaded_path = os.path.join(downloads_path, path_format(font['category']), path_format(font['theme']), path_format(font['creator']), path_format(font['name']))

    for root, _, files in os.walk(downloaded_path):
      for f in files:
        if '.' in f:

          dest_file_name = path_format(f, allow_dots=True)
          file_type = f.split('.')[-1].lower()

          if file_type == 'ttf' or file_type == 'otf':
            shutil.copyfile(os.path.join(root, f), os.path.join(fonts_output, dest_file_name))
            csv_file.write('\r\n')
            csv_file.write(f"{dest_file_name},{font['name']},{file_type},{font['creator']},{font['category']},{font['theme']}")
            all_font_creators.append(font['creator'])
            num_fonts.append(dest_file_name)

          if print_extension_info:
            if file_type in extensions:
              extensions[file_type] += 1
            else:
              extensions[file_type] = 1

  if print_extension_info:
    extensions = dict(sorted(extensions.items(), key=lambda x:x[1]))
    print(extensions)

  csv_file.close()

  num_fonts = len(list(set(num_fonts)))

  readme = open(os.path.join(output, 'readme.txt'), 'w')
  readme.write(f'Dafonts Free Dataset\nThis is a dataset of {num_fonts} fonts labeled as `100% Free` and `Public domain / GPL / OFL` on https://www.dafont.com/ with `.ttf` and `.otf\nCode used to create it can be found at: https://github.com/duskvirkus/dafonts-free\nThis version was created based on download links scraped from dafont.com on {date_scraped}\n')
  readme.write('Citation information:\n@misc{dafonts-free,\n  title         = {Dafonts Free Dataset},\n  year          = {6 March 2022},\n  url           = {https://github.com/duskvirkus/dafonts-free}\n  author        = {D. Virkus},\n}\n')

  # dedupe creator list
  all_font_creators = list(set(all_font_creators))
  all_font_creators_str = ''
  for c in all_font_creators:
    all_font_creators_str += c
    all_font_creators_str += '\n'

  readme.write(f'All Font Creators:\n{all_font_creators_str}\n')
  readme.close()

if __name__ == '__main__':
  dist()