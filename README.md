# DaFonts Free Dataset

This is the git repository associated the dafonts-free dataset. A dataset constructed of fonts labeled as `100% Free` and `Public domain / GPL / OFL` on https://www.dafont.com/ with `.ttf` and `.otf` extensions.

![Header image says dafonts free in changing fonts.](dafonts-free-header.gif)

This repository includes the python code used to collect and organize the dataset. 

The dataset it's self is available as a zip file containing a `.csv` file with font metadata including filename, base_font_name, file_format, creator, category, and theme. 

Dataset is provided as-is (stated in the license) and if possible credit the creators the fonts in any project you use this dataset for.

## Download Dataset

GitHub Release: _
archive.org: _
gdown id: _

## Running Scripts

### Setup

Install chrome/chromium

Get driver from https://sites.google.com/chromium.org/driver/

```bash
conda create -n dafont-scraper python=3.8
conda activate dafont-scraper
pip install -r requirements.txt
```

### Usage

```bash
python create_font_list.py --help
```

```bash
python download.py --help
```

```bash
python dist.py --help
```

## Citation

```bibtex
@misc{dafonts-free,
  title         = {Dafonts Free Dataset},
  year          = {6 March 2022},
  url           = {https://github.com/duskvirkus/dafonts-free}
  author        = {D. Virkus},
}
```
