import click
import os

click.command()
@click.option(
  '-o',
  '--output',
  type=click.Path(exists=False),
  help='The root directory for dist.',
  default=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dist')),
  show_default=True,
)
def dist(
  output
):
  os.makedirs(output)

if __name__ == '__main__':
  dist()