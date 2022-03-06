import re

def path_format(a, allow_dots=False):
  a = a.lower().strip().replace(' ', '_')
  if allow_dots:
    a = re.sub('\s', '', a)
  else:
    a = re.sub('\W', '', a)
  return a