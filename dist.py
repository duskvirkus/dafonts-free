import click
import os
import shutil
import json

from utils import path_format

def is_font_ext(file_name):
  if not '.' in file_name:
    return False

  extension = file_name.split('.')[-1].lower()

  if extension == 'ttf' or extension == 'otf' or extension == 'woff' or extension == 'woff2' or extension == 'eot' or extension == 'pfb' or extension == 'dfont':
    return True
  elif extension == 'pdf' or extension == 'txt' or extension == 'jpg' or extension == 'png' or extension == 'gif' or extension == 'html' or extension == 'psd' or extension == 'htm' or extension == 'rtf' or extension == 'svg' or extension == 'doc' or extension == 'url' or extension == 'bmp' or extension == 'wps' or extension == 'pfm' or extension == 'nfo' or extension == 'afm' or extension == 'ai' or extension == 'jpeg' or extension == 'inf' or extension == 'wri' or extension == 'sfd' or extension == 'bin' or extension == 'css' or extension == 'license' or extension == 'readme' or extension == 'docx' or extension == 'ds_store' or extension == 'md' or extension == 'changelog' or extension == 'exe' or extension == 'js' or extension == 'read me!' or extension == 'pin pon pin pon pin pon' or extension == '3o9' or extension == 'peace':
    return False

  print(f'WARNING! unexpected file format {extension}')
  return False

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
def dist(
  output,
  input,
  downloads_path,
):
  project_root = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))

  os.makedirs(output)

  shutil.copyfile(os.path.join(project_root, 'LICENCE.md'), os.path.join(output, 'LICENCE.md'))

  csv_file = open(os.path.join(output, 'info.csv'), 'w')

  csv_file.write('filename,base_font_name,file_format,creator,category,theme')

  f = open(input, 'r')
  data = json.load(f)

  count = 0
  for font in data['font_info']:
    downloaded_path = os.path.join(downloads_path, path_format(font['category']), path_format(font['theme']), path_format(font['creator']), path_format(font['name']))

    for root, _, files in os.walk(downloaded_path):
      for f in files:
        # print(root)
        # print(f)

        file_type = f.split('.')[-1].lower()
        # print(file_type)

        if is_font_ext(f):
          pass

    # count += 1
    # if count > 1000:
    #   break


  csv_file.close()

if __name__ == '__main__':
  dist()