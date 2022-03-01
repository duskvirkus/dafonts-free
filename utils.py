import re

def path_format(a):
  a = a.lower().strip().replace(' ', '_')
  a = re.sub('\W', '', a)
  return a